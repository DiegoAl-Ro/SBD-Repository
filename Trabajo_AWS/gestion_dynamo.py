# Imports necesarios
import os
import json
from decimal import Decimal
import boto3
from boto3.dynamodb.conditions import Key, Attr
from dotenv import load_dotenv

# Cargamos el load
load_dotenv

# Inicializamos los recursos y clientes de DynamoDB
# boto3 lee automáticamente AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN y AWS_DEFAULT_REGION
dynamodb_resource = boto3.resource('dynamodb')
dynamodb_client = boto3.client('dynamodb')

# Creamos variables para las 3 tablas, por si debemos cambiarles el nombre en el futuro
TABLA_CAMIONES = "CleanClan_Camiones"
TABLA_LECTURAS = "CleanClan_Lecturas"
TABLA_INCIDENCIAS = "CleanClan_Incidencias"

# Usaremos helper para convertir objetos Decimal de DynamoDB a float/int al imprimir en JSON
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return int(obj) if obj % 1 == 0 else float(obj)
        return super(DecimalEncoder, self).default(obj)

# Crearemos una función que convertirá los datos en json
def formatear_json(datos):
    return json.dumps(datos, indent=4, ensure_ascii=False, cls=DecimalEncoder)

# Crearemos las 3 tablas(Sin índice y con índice local/global)
def crear_tablas():
    tablas_existentes = dynamodb_client.list_tables()['TableNames']

    # 1. Tabla SIN índices secundarios (Solo Partition Key: matricula)
    if TABLA_CAMIONES not in tablas_existentes:
        print(f"Creando tabla {TABLA_CAMIONES} (sin índices)...")
        table1 = dynamodb_resource.create_table(
            TableName=TABLA_CAMIONES,
            KeySchema=[{'AttributeName': 'matricula', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'matricula', 'AttributeType': 'S'}],
            BillingMode='PAY_PER_REQUEST'
        )
        table1.wait_until_exists()
        print(f"Tabla {TABLA_CAMIONES} creada correctamente.")
    else:
        print(f"La tabla {TABLA_CAMIONES} ya existe.")

    # 2. Tabla CON Índice Local
    # PK: id_sensor, SK: timestamp, LSI: LSI_NivelLlenado (id_sensor + porcentaje_lleno)
    if TABLA_LECTURAS not in tablas_existentes:
        print(f"Creando tabla {TABLA_LECTURAS} (con Índice Local LSI)...")
        table2 = dynamodb_resource.create_table(
            TableName=TABLA_LECTURAS,
            KeySchema=[
                {'AttributeName': 'id_sensor', 'KeyType': 'HASH'},
                {'AttributeName': 'timestamp', 'KeyType': 'RANGE'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'id_sensor', 'AttributeType': 'N'},
                {'AttributeName': 'timestamp', 'AttributeType': 'S'},
                {'AttributeName': 'porcentaje_lleno', 'AttributeType': 'N'}
            ],
            LocalSecondaryIndexes=[
                {
                    'IndexName': 'LSI_NivelLlenado',
                    'KeySchema': [
                        {'AttributeName': 'id_sensor', 'KeyType': 'HASH'},
                        {'AttributeName': 'porcentaje_lleno', 'KeyType': 'RANGE'}
                    ],
                    'Projection': {'ProjectionType': 'ALL'}
                }
            ],
            BillingMode='PAY_PER_REQUEST'
        )
        table2.wait_until_exists()
        print(f"Tabla {TABLA_LECTURAS} creada correctamente.")
    else:
        print(f"La tabla {TABLA_LECTURAS} ya existe.")

    # 3. Tabla CON Índice Global
    # PK: id_incidencia,, GSI: GSI_EstadoResolucion (estado_resolucion)
    if TABLA_INCIDENCIAS not in tablas_existentes:
        print(f"Creando tabla {TABLA_INCIDENCIAS} (con Índice Global GSI)...")
        table3 = dynamodb_resource.create_table(
            TableName=TABLA_INCIDENCIAS,
            KeySchema=[{'AttributeName': 'id_incidencia', 'KeyType': 'HASH'}],
            AttributeDefinitions=[
                {'AttributeName': 'id_incidencia', 'AttributeType': 'S'},
                {'AttributeName': 'estado_resolucion', 'AttributeType': 'S'}
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'GSI_EstadoResolucion',
                    'KeySchema': [
                        {'AttributeName': 'estado_resolucion', 'KeyType': 'HASH'}
                    ],
                    'Projection': {'ProjectionType': 'ALL'}
                }
            ],
            BillingMode='PAY_PER_REQUEST'
        )
        table3.wait_until_exists()
        print(f"Tabla {TABLA_INCIDENCIAS} creada correctamente.")
    else:
        print(f"La tabla {TABLA_INCIDENCIAS} ya existe.")

# Con lkas tablas ya creadas insertaremos 3 registros en cada una
def insertar_registros():
    t_camiones = dynamodb_resource.Table(TABLA_CAMIONES)
    t_lecturas = dynamodb_resource.Table(TABLA_LECTURAS)
    t_incidencias = dynamodb_resource.Table(TABLA_INCIDENCIAS)

    # 3 Camiones (coincide '1234-BCD' con el de RDS para cruzar datos luego)
    camiones = [
        {'matricula': '1234-BCD', 'modelo': 'Volvo FE', 'combustible_pct': 80, 'estado': 'Operativo'},
        {'matricula': '5678-FGH', 'modelo': 'Mercedes Econic', 'combustible_pct': 35, 'estado': 'Operativo'},
        {'matricula': '9012-JKL', 'modelo': 'Iveco Eurocargo', 'combustible_pct': 15, 'estado': 'Taller'}
    ]
    for c in camiones:
        t_camiones.put_item(Item=c)

    # 3 Lecturas de Sensores (coincide id_sensor=1 con RDS)
    lecturas = [
        {'id_sensor': 1, 'timestamp': '2026-11-16T08:00:00', 'porcentaje_lleno': 92, 'temperatura': Decimal('24.5')},
        {'id_sensor': 1, 'timestamp': '2026-11-16T12:00:00', 'porcentaje_lleno': 45, 'temperatura': Decimal('26.0')},
        {'id_sensor': 2, 'timestamp': '2026-11-16T10:30:00', 'porcentaje_lleno': 88, 'temperatura': Decimal('22.1')}
    ]
    for l in lecturas:
        t_lecturas.put_item(Item=l)

    # 3 Incidencias
    incidencias = [
        {'id_incidencia': 'INC-001', 'id_sensor': 1, 'tipo': 'Contenedor Lleno', 'estado_resolucion': 'Pendiente', 'prioridad': 'Alta'},
        {'id_incidencia': 'INC-002', 'id_sensor': 2, 'tipo': 'Tapa Rota', 'estado_resolucion': 'En Proceso', 'prioridad': 'Media'},
        {'id_incidencia': 'INC-003', 'id_sensor': 1, 'tipo': 'Mal Olor', 'estado_resolucion': 'Resuelto', 'prioridad': 'Baja'}
    ]
    for i in incidencias:
        t_incidencias.put_item(Item=i)

    print("Se han insertado 3 registros correctamente en cada una de las 3 tablas.")

# Obtendremos un registro de cada tabla
def obtener_un_registro():
    res_camion = dynamodb_resource.Table(TABLA_CAMIONES).get_item(Key={'matricula': '1234-BCD'}).get('Item')
    res_lectura = dynamodb_resource.Table(TABLA_LECTURAS).get_item(Key={'id_sensor': 1, 'timestamp': '2026-11-16T08:00:00'}).get('Item')
    res_incidencia = dynamodb_resource.Table(TABLA_INCIDENCIAS).get_item(Key={'id_incidencia': 'INC-001'}).get('Item')

    return formatear_json({
        "Camion_Obtenido": res_camion,
        "Lectura_Obtenida": res_lectura,
        "Incidencia_Obtenida": res_incidencia
    })

# Actualizaremos un registro de cada tabla
def actualizar_registros():
    # Actualizamos el combustible del camión 1234-BCD
    r1 = dynamodb_resource.Table(TABLA_CAMIONES).update_item(
        Key={'matricula': '1234-BCD'},
        UpdateExpression="SET combustible_pct = :val",
        ExpressionAttributeValues={':val': 95},
        ReturnValues="UPDATED_NEW"
    )
    # Actualizar porcentaje_lleno de la lectura de las 12:00
    r2 = dynamodb_resource.Table(TABLA_LECTURAS).update_item(
        Key={'id_sensor': 1, 'timestamp': '2026-11-16T12:00:00'},
        UpdateExpression="SET porcentaje_lleno = :val",
        ExpressionAttributeValues={':val': 60},
        ReturnValues="UPDATED_NEW"
    )
    # Actualizar estado de INC-002 a Resuelto
    r3 = dynamodb_resource.Table(TABLA_INCIDENCIAS).update_item(
        Key={'id_incidencia': 'INC-002'},
        UpdateExpression="SET estado_resolucion = :val",
        ExpressionAttributeValues={':val': 'Resuelto'},
        ReturnValues="UPDATED_NEW"
    )
    return formatear_json({
        "Camion_Actualizado": r1.get('Attributes'),
        "Lectura_Actualizada": r2.get('Attributes'),
        "Incidencia_Actualizada": r3.get('Attributes')
    })

# Eliminaremos un registro de cada tabla
def eliminar_un_registro():
    # Insertamos primero un registro temporal en cada tabla para no vaciar los datos principales
    dynamodb_resource.Table(TABLA_CAMIONES).put_item(Item={'matricula': 'TEMP-000', 'modelo': 'Test', 'combustible_pct': 10, 'estado': 'Baja'})
    dynamodb_resource.Table(TABLA_LECTURAS).put_item(Item={'id_sensor': 99, 'timestamp': '2026-01-01T00:00:00', 'porcentaje_lleno': 0, 'temperatura': Decimal('15.0')})
    dynamodb_resource.Table(TABLA_INCIDENCIAS).put_item(Item={'id_incidencia': 'INC-TEMP', 'id_sensor': 99, 'tipo': 'Prueba', 'estado_resolucion': 'Descartado', 'prioridad': 'Baja'})

    # Eliminamos esos 3 registros
    dynamodb_resource.Table(TABLA_CAMIONES).delete_item(Key={'matricula': 'TEMP-000'})
    dynamodb_resource.Table(TABLA_LECTURAS).delete_item(Key={'id_sensor': 99, 'timestamp': '2026-01-01T00:00:00'})
    dynamodb_resource.Table(TABLA_INCIDENCIAS).delete_item(Key={'id_incidencia': 'INC-TEMP'})

    return "Se ha eliminado 1 registro de prueba en cada una de las 3 tablas correctamente."

# Obtener todos los registros de cada tabla
def obtener_todos():
    c = dynamodb_resource.Table(TABLA_CAMIONES).scan().get('Items', [])
    l = dynamodb_resource.Table(TABLA_LECTURAS).scan().get('Items', [])
    i = dynamodb_resource.Table(TABLA_INCIDENCIAS).scan().get('Items', [])

    return formatear_json({
        "Todos_Camiones": c,
        "Todas_Lecturas": l,
        "Todas_Incidencias": i
    })

# Filtraremos usando scan
def filtrar_con_scan_y_gsi():
    # Tabla 1 (Scan con filtro simple)
    c_filtrados = dynamodb_resource.Table(TABLA_CAMIONES).scan(
        FilterExpression=Attr('estado').eq('Operativo')
    ).get('Items', [])

    # Tabla 2 (Scan con filtro simple)
    l_filtradas = dynamodb_resource.Table(TABLA_LECTURAS).scan(
        FilterExpression=Attr('porcentaje_lleno').gt(80)
    ).get('Items', [])

    # Tabla 3 (Scan sobre el Índice Global GSI_EstadoResolucion)
    i_filtradas = dynamodb_resource.Table(TABLA_INCIDENCIAS).scan(
        IndexName='GSI_EstadoResolucion',
        FilterExpression=Attr('estado_resolucion').eq('Pendiente')
    ).get('Items', [])

    return formatear_json({
        "Camiones_Operativos_Scan": c_filtrados,
        "Lecturas_Criticas_Scan": l_filtradas,
        "Incidencias_Pendientes_GSI": i_filtradas
    })

# Eliminaremos cada tabla
def eliminacion_condicional():
    # Insertamos 3 registros candidatos a ser borrados condicionalmente
    dynamodb_resource.Table(TABLA_CAMIONES).put_item(Item={'matricula': 'DEL-111', 'modelo': 'Viejo', 'combustible_pct': 5, 'estado': 'Desguace'})
    dynamodb_resource.Table(TABLA_LECTURAS).put_item(Item={'id_sensor': 50, 'timestamp': '2026-11-16T01:00:00', 'porcentaje_lleno': 5, 'temperatura': Decimal('10.0')})
    dynamodb_resource.Table(TABLA_INCIDENCIAS).put_item(Item={'id_incidencia': 'INC-DEL', 'id_sensor': 50, 'tipo': 'Falsa Alarma', 'estado_resolucion': 'Obsoleta', 'prioridad': 'Baja'})

    # 1. Borrado condicional en Camiones (solo si estado == 'Desguace')
    dynamodb_resource.Table(TABLA_CAMIONES).delete_item(
        Key={'matricula': 'DEL-111'},
        ConditionExpression=Attr('estado').eq('Desguace')
    )

    # 2. Borrado condicional en Lecturas (solo si porcentaje_lleno < 10)
    dynamodb_resource.Table(TABLA_LECTURAS).delete_item(
        Key={'id_sensor': 50, 'timestamp': '2026-11-16T01:00:00'},
        ConditionExpression=Attr('porcentaje_lleno').lt(10)
    )

    # 3. Borrado condicional en Incidencias localizando primero mediante el Índice Global (GSI)
    tabla_inc = dynamodb_resource.Table(TABLA_INCIDENCIAS)
    items_gsi = tabla_inc.query(
        IndexName='GSI_EstadoResolucion',
        KeyConditionExpression=Key('estado_resolucion').eq('Obsoleta')
    ).get('Items', [])

    for item in items_gsi:
        tabla_inc.delete_item(
            Key={'id_incidencia': item['id_incidencia']},
            ConditionExpression=Attr('estado_resolucion').eq('Obsoleta')
        )

    return "Eliminación condicional completada en las 3 tablas (utilizando GSI en Incidencias)."

# Obtendremos datos con varios filtros aplicados a cada tabla
def filtrar_multiples_condiciones():
    # Tabla 1: Estado Operativo Y combustible > 50%
    c_multi = dynamodb_resource.Table(TABLA_CAMIONES).scan(
        FilterExpression=Attr('estado').eq('Operativo') & Attr('combustible_pct').gt(50)
    ).get('Items', [])

    # Tabla 2: id_sensor == 1 Y porcentaje_lleno >= 50 (usando el Índice Local LSI_NivelLlenado)
    l_multi = dynamodb_resource.Table(TABLA_LECTURAS).query(
        IndexName='LSI_NivelLlenado',
        KeyConditionExpression=Key('id_sensor').eq(1) & Key('porcentaje_lleno').gte(50)
    ).get('Items', [])

    # Tabla 3: estado_resolucion == 'Pendiente' Y prioridad == 'Alta'
    i_multi = dynamodb_resource.Table(TABLA_INCIDENCIAS).scan(
        FilterExpression=Attr('estado_resolucion').eq('Pendiente') & Attr('prioridad').eq('Alta')
    ).get('Items', [])

    return formatear_json({
        "Camiones_Operativos_Con_Combustible": c_multi,
        "Lecturas_Sensor1_Altas_LSI": l_multi,
        "Incidencias_Pendientes_Urgentes": i_multi
    })

# Ejecutaremos consultas con partiQL statement en cada tabla
def consultas_partiql():
    # PartiQL sobre Tabla 1
    res1 = dynamodb_client.execute_statement(
        Statement=f"SELECT * FROM \"{TABLA_CAMIONES}\" WHERE estado = 'Operativo'"
    ).get('Items', [])

    # PartiQL sobre Tabla 2
    res2 = dynamodb_client.execute_statement(
        Statement=f"SELECT * FROM \"{TABLA_LECTURAS}\" WHERE id_sensor = 1"
    ).get('Items', [])

    # PartiQL sobre Tabla 3
    res3 = dynamodb_client.execute_statement(
        Statement=f"SELECT * FROM \"{TABLA_INCIDENCIAS}\" WHERE prioridad = 'Alta'"
    ).get('Items', [])

    return formatear_json({
        "PartiQL_Camiones": res1,
        "PartiQL_Lecturas": res2,
        "PartiQL_Incidencias": res3
    })