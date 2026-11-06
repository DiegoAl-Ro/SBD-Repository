import mysql.connector
import psycopg2
import redis

MYSQL_CONFIG = {'host': 'localhost', 'port': 3306, 'user': 'cleanuser', 'password': 'cleanpw', 'database': 'cleanclan_db'}
POSTGRES_CONFIG = {'host': 'localhost', 'port': 5432, 'user': 'cleanuser', 'password': 'cleanpw', 'dbname': 'cleanclan_db'}
bd = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

print("EJERCICIO 21: MIGRAR DATOS DESDE SQL (MySQL) A REDIS")
print("Explicación: Consultamos la tabla 'empleados' de MySQL mediante SQL e insertamos cada fila en Hashes de Redis.")

try:
    conn_sql = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = conn_sql.cursor(dictionary=True)
    cursor.execute("SELECT id_empleado, nombre, apellido, dni, cargo FROM empleados;")
    empleados = cursor.fetchall()

    for emp in empleados:
        clave_redis = f"sql:empleado:{emp['id_empleado']}"
        bd.hset(clave_redis, mapping={
            "nombre": emp["nombre"],
            "apellido": emp["apellido"],
            "dni": emp["dni"],
            "cargo": emp["cargo"]
        })
    
    cursor.close()
    conn_sql.close()
    print(f"Se han migrado {len(empleados)} empleados de MySQL a Redis correctamente.")
    print("Ejemplo de clave creada en Redis ('sql:empleado:1'):")
    print(f"{bd.hgetall('sql:empleado:1')}\n")
except Exception as e:
    print(f"Error en Ejercicio 21: {e}\n")


print("EJERCICIO 22: MIGRAR DATOS DESDE REDIS A SQL (PostgreSQL)")
print("Explicación: Leemos los datos de sensores generados en Redis y los exportamos a la tabla 'sensores_iot' de PostgreSQL.")

try:
    claves_sensores = bd.keys('sensor:*')
    
    conn_pg = psycopg2.connect(**POSTGRES_CONFIG)
    cursor_pg = conn_pg.cursor()
    
    insertados = 0
    for c in claves_sensores:
        datos = bd.hgetall(c)
        if datos and 'modelo' in datos:
            cursor_pg.execute(
                "INSERT INTO sensores_iot (id_contenedor, modelo, porcentaje_bateria, estado) VALUES (%s, %s, %s, %s)",
                (1, datos.get('modelo', 'Sensor-Redis'), int(datos.get('bateria', 50)), datos.get('estado', 'Activo'))
            )
            insertados += 1
            
    conn_pg.commit()
    cursor_pg.close()
    conn_pg.close()
    print(f"-> Efecto: Se exportaron {insertados} registros desde Redis hacia la tabla 'sensores_iot' en PostgreSQL.\n")
except Exception as e:
    print(f"Error en Ejercicio 22: {e}\n")