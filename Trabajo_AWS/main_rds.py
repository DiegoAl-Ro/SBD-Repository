import gestion_rds as rds

def main():
    print("\n-- EJECUTANDO ESTRCUTURA RDS PARA AWS --\n")

    print("Paso 1: Creando Base de Datos en RDS...")
    rds.crear_bd()
    
    print("\nPaso 2: Creando Tablas del Proyecto CleanClan...")
    rds.crear_tablas()
    
    print("\nPaso 3: Insertando Registros de Prueba...")
    rds.poblar_datos_prueba()
    
    print("\nEJECUTANDO CONSULTA 1: Empleados Registrados")
    print(rds.consulta_empleados())
    
    print("\nEJECUTANDO CONSULTA 2: Lecturas de Sensores Críticos")
    print(rds.consulta_sensores_criticos())
    print("\nEJECUTANDO CONSULTA 3: Infraestructura y Contenedores")
    print(rds.consulta_infraestructura_completa())

    print("\nPROCESO TERMINADO")

if __name__ == "__main__":
    main()