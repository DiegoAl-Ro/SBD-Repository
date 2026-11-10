import gestion_rds as rds

def main():
    print("-- EJECUTANDO ESTRCUTURA RDS PARA AWS --")

    print("Paso 1: Creando Base de Datos en RDS...")
    rds.crear_bd()
    
    print("\nPaso 2: Creando Tablas del Proyecto CleanClan...")
    rds.crear_tablas()
    
    print("\nPaso 3: Insertando Registros de Prueba...")
    rds.poblar_datos_iniciales()
    
    print("\nEJECUTANDO CONSULTA 1: Empleados Registrados")
    print(rds.consulta_1_empleados_json())
    
    print("\nEJECUTANDO CONSULTA 2: Lecturas de Sensores Críticos")
    print(rds.consulta_2_sensores_criticos_json())

    print("\nEJECUTANDO CONSULTA 3: Infraestructura y Contenedores")
    print(rds.consulta_3_infraestructura_completa_json())

    print("\nPROCESO TERMINADO")

if __name__ == "__main__":
    main()