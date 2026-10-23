import json
import mysql.connector
import psycopg2

MYSQL_CONFIG = {'host': 'localhost', 'port': 3306, 'user': 'cleanuser', 'password': 'cleanpw', 'database': 'cleanclan_db'}
POSTGRES_CONFIG = {'host': 'localhost', 'port': 5432, 'user': 'cleanuser', 'password': 'cleanpw', 'dbname': 'cleanclan_db'}
MARIADB_CONFIG = {'host': 'localhost', 'port': 3307, 'user': 'cleanuser', 'password': 'cleanpw', 'database': 'cleanclan_db'}

QUERY_MYSQL = """
SELECT b.nombre AS barrio, pr.direccion, tr.nombre AS tipo_residuo, s.porcentaje_bateria, l.porcentaje_lleno, l.timestamp_lectura
FROM lecturas_sensores l
JOIN sensores_iot s ON l.id_sensor = s.id_sensor
JOIN contenedores c ON s.id_contenedor = c.id_contenedor
JOIN tipo_residuos tr ON c.id_tipo_residuo = tr.id_tipo_residuo
JOIN puntos_recogida pr ON c.id_punto = pr.id_punto
JOIN barrios b ON pr.id_barrio = b.id_barrio
WHERE l.porcentaje_lleno > 70;
"""

QUERY_POSTGRES = """
SELECT r.id_ruta, b.nombre AS barrio, e.nombre AS conductor_nombre, e.apellido AS conductor_apellido, c.matricula AS camion_matricula, r.fecha_ruta, r.estado_ruta
FROM rutas_recogida r
JOIN barrios b ON r.id_barrio = b.id_barrio
JOIN empleados e ON r.id_empleado = e.id_empleado
JOIN camiones c ON r.id_camion = c.id_camion;
"""

QUERY_MARIADB = """
SELECT i.id_incidencia, b.nombre AS barrio, pr.direccion, i.tipo AS tipo_incidencia, i.estado_resolucion, i.fecha_reporte
FROM incidencias i
JOIN puntos_recogida pr ON i.id_punto = pr.id_punto
JOIN barrios b ON pr.id_barrio = b.id_barrio
WHERE i.estado_resolucion != 'Resuelto';
"""

def exportar_json_mysql():
    conn = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = conn.cursor(dictionary=True)
    cursor.execute(QUERY_MYSQL)
    datos = cursor.fetchall()
    for d in datos:
        d['timestamp_lectura'] = str(d['timestamp_lectura'])
    with open('analisis_contenedores_criticos_mysql.json', 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)
    print("Creado: analisis_contenedores_criticos_mysql.json")

def exportar_json_postgres():
    conn = psycopg2.connect(**POSTGRES_CONFIG)
    cursor = conn.cursor()
    cursor.execute(QUERY_POSTGRES)
    columnas = [desc[0] for desc in cursor.description]
    filas = cursor.fetchall()
    datos = [dict(zip(columnas, fila)) for fila in filas]
    for d in datos:
        d['fecha_ruta'] = str(d['fecha_ruta'])
    with open('rendimiento_rutas_conductores_postgres.json', 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)
    print("Creado: rendimiento_rutas_conductores_postgres.json")

def exportar_json_mariadb():
    conn = mysql.connector.connect(**MARIADB_CONFIG)
    cursor = conn.cursor(dictionary=True)
    cursor.execute(QUERY_MARIADB)
    datos = cursor.fetchall()
    for d in datos:
        d['fecha_reporte'] = str(d['fecha_reporte'])
    with open('incidencias_pendientes_mariadb.json', 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)
    print("Creado: incidencias_pendientes_mariadb.json")

if __name__ == "__main__":
    print("=== EXPORTANDO CONSULTAS A JSON ===")
    exportar_json_mysql()
    exportar_json_postgres()
    exportar_json_mariadb()