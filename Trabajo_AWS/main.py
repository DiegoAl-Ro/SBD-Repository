# Este script es el main principal, hecho para ejecutar todo en orden automáticamente

# Imports necesarios
import main_rds
import main_dynamo
import unir_datos
import gestion_dynamo as dynamo

def ejecucion_total():
    print("-- INICIANDO DESPLIEGUE COMPLETO CLEANCLAN EN AWS --")

    # 1. Creamos la base de datos relacional en Amazon RDS (MySQL)
    print("1. Creando estructura y datos en Amazon RDS...")
    main_rds.main()

    # 2. Creamos las tablas NoSQL, índices y consultas en Amazon DynamoDB
    print("\n2. Desplegando tablas, índices y operaciones en DynamoDB...")
    main_dynamo.main()

    # 3. Hacemos el cruce híbrido de datos (RDS + DynamoDB) y exportación a JSON
    print("\n3. Uniendo datos de RDS y DynamoDB...")
    resultado_global = {
        "proyecto": "CleanClan - Arquitectura Híbrida AWS",
        "flota_camiones": unir_datos.datos_camiones(),
        "red_sensores_iot": unir_datos.datos_sensores()
    }

    json_final = dynamo.formatear_json(resultado_global)
    print(json_final)

    with open("cleanclan_unificado.json", "w", encoding="utf-8") as f:
        f.write(json_final)

    print("-- DESPLIEGUE COMPLETADO: 'cleanclan_unificado.json' CREADO --")


if __name__ == "__main__":
    ejecucion_total()