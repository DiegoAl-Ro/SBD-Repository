# Script encargado de juntar datos relacionados entre bdd de RDS y tablas únicaas de Dynamo

# Imports necesarios
import json
import gestion_rds as rds
import gestion_dynamo as dynamo

# Esta función unirá los datos de los camiones entre rds y las tablas de dynamo
def datos_camiones():

    try:
        conn = rds.obtener_conexion(incluir_db=True)
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"SELECT id_camion, matricula, modelo, capacidad_toneladas FROM camiones;")
        camiones_rds = cursor.fetchall()
        cursor.close()
        conn.close()

        camiones_dynamo = dynamo.dynamodb_resource.Table(dynamo.TABLA_CAMIONES).scan().get('Items', [])

        seguimiento_por_matricula = {c['matricula']: c for c in camiones_dynamo}

        camiones_unidos = []
        for camion in camiones_rds:
            mat = camion['matricula']
            datos_tiempo_real = seguimiento_por_matricula.get(mat, {})

            camiones_unidos.append({
                "id_camion": camion['id_camion'],
                "matricula": mat,
                "modelo": camion['modelo'],
                "capacidad_toneladas": float(camion['capacidad_toneladas']),
                "combustible_pct": datos_tiempo_real.get('combustible_pct', 'Sin datos'),
                "estado_actual": datos_tiempo_real.get('estado', 'Desconocido')
            })

        return camiones_unidos
    
    except Exception as e:
        print(f"Error al unir datos de Camiones entre RDS y Dynamo: {e}")
        raise e

# Esta función unirá los datos de los sensores e incidencias entre rds y las tablas de dynamo
def datos_sensores():

    try:
        conn = rds.obtener_conexion(incluir_db=True)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT s.id_sensor, s.modelo, s.porcentaje_bateria, p.direccion, b.nombre AS barrio
            FROM sensores_iot s
            JOIN contenedores c ON s.id_contenedor = c.id_contenedor
            JOIN puntos_recogida p ON c.id_punto = p.id_punto
            JOIN barrios b ON p.id_barrio = b.id_barrio;
        """)
        sensores_rds = cursor.fetchall()
        cursor.close()
        conn.close()

        lecturas_dynamo = dynamo.dynamodb_resource.Table(dynamo.TABLA_LECTURAS).scan().get('Items', [])
        incidencias_dynamo = dynamo.dynamodb_resource.Table(dynamo.TABLA_INCIDENCIAS).scan().get('Items', [])

        sensores_unidos = []
        for sensor in sensores_rds:
            id_s = sensor['id_sensor']

            lecturas_sensor = [l for l in lecturas_dynamo if l.get('id_sensor') == id_s]
            incidencias_sensor = [i for i in incidencias_dynamo if i.get('id_sensor') == id_s]

            sensores_unidos.append({
                "id_sensor": id_s,
                "modelo": sensor['modelo'],
                "ubicacion": f"{sensor['direccion']} ({sensor['barrio']})",
                "porcentaje_bateria": float(sensor['porcentaje_bateria']),
                "historial_lecturas_dynamo": lecturas_sensor,
                "incidencias_dynamo": incidencias_sensor
            })
            
        return sensores_unidos
                
    except Exception as e:
        print(f"Error al unir datos de Sensores e Incidencias entre RDS y Dynamo: {e}")
        raise e

if __name__ == "__main__":
    print("\n-- UNIFICANDO DATOS HÍBRIDOS CLEANCLAN (RDS + DYNAMODB) --\n")
    
    resultado_global = {
        "proyecto": "CleanClan - Arquitectura Híbrida AWS",
        "flota_camiones": datos_camiones(),
        "red_sensores_iot": datos_sensores()
    }

    # Usamos el formatear_json de gestion_dynamo para convertir los Decimal automáticamente
    json_final = dynamo.formatear_json(resultado_global)
    print(json_final)

    with open("cleanclan_unificado.json", "w", encoding="utf-8") as f:
        f.write(json_final)
    
    print("\nArchivo 'cleanclan_unificado.json' generado correctamente.")