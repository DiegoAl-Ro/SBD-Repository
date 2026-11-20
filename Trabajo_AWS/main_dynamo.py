# Este script ejecutará todas las funciones de gestion_dynamo.py y confirmará su éxito

# Import necesario del script con las funciones
import gestion_dynamo as dynamo

# Función principal para ejecutar todo encadenado
def main():
    print("\n-- EJECUTANDO ESTRUCTURA DYNAMO PARA AWS --\n")

    print("Paso 1: Creando las 3 tablas(Sin índice y con índice local/global) con Dynamo...")
    dynamo.crear_tablas()

    print("\nPaso 2: Creando 3 registros en cada tabla...")
    dynamo.insertar_registros()

    print("\nEJECUTANDO CONSULTA 1: Obteniendo un registro de cada tabla...")
    print(dynamo.obtener_un_registro())

    print("\nEJECUTANDO CONSULTA 2: Actualizando un registro en cada tabla...")
    print(dynamo.actualizar_registros())

    print("\nEJECUTANDO CONSULTA 3: Eliminando un registro en cada tabla...")
    print(dynamo.eliminar_un_registro())

    print("\nEJECUTANDO CONSULTA 4: Obteniendo todos los registros de cada tabla...")
    print(dynamo.obtener_todos())

    print("\nEJECUTANDO CONSULTA 5: Obteniendo registros con filtrado scan...")
    print(dynamo.filtrar_con_scan_y_gsi())

    print("\nEJECUTANDO CONSULTA 6: Realizando una eliminación condicional en cada tabla...")
    print(dynamo.eliminacion_condicional())

    print("\nEJECUTANDO CONSULTA 7: Obteniendo un conjunto de datos cn filtro...")
    print(dynamo.filtrar_multiples_condiciones())

    print("\nEJECUTANDO CONSULTA 8: Utilizando PartiQL en cada tabla...")
    print(dynamo.consultas_partiql())

    print("\nPROCESO TERMINADO")

if __name__ == "__main__":
    main()