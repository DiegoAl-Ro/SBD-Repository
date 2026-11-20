# CleanClan - Arquitectura Híbrida en AWS (RDS + DynamoDB)

Proyecto de unión de datos híbridos para la gestión de recogida de residuos urbanos (CleanClan), conectado a Amazon RDS (MySQL) y NoSQL en Amazon DynamoDB.

## Estructura del Proyecto

* `gestion_rds.py` / `main_rds.py`: Creación de la base de datos `cleanclandb`, sus 8 tablas relacionales, inserción de registros iniciales y consultas SQL con `JOIN`.
* `gestion_dynamo.py` / `main_dynamo.py`: Despliegue de 3 tablas en DynamoDB (sin índices, con Índice Local `LSI` y con Índice Global `GSI`), operaciones CRUD, filtros `scan`/`query`, borrado condicional y consultas `PartiQL`.
* `unir_datos.py`: Módulo integrador que cruza la información maestra de RDS con la telemetría en tiempo real de DynamoDB.
* `main.py`: **Orquestador principal** que ejecuta todo el flujo de trabajo de principio a fin.
* `cleanclan_unificado.json`: Salida JSON generada con los datos unificados de camiones, sensores e incidencias.

## Pasos para Ejecución

1. Activar el entorno virtual e instalar rquisitos:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. Ejecutar el proyecyo:

    ```python3 main.py
    ```