# Este script se encargará de conectar la aws con rds y crear las tablas

# Imports necesarios
import os
import json
import mysql.connector
from dotenv import load_dotenv

# Cargamos el dotenv para poder leer los datos de la bdd
load_dotenv()

# Especificamos el nombre de la bdd
DB_NAME = os.getenv('DB_NAME')

# Creamos la función que conectará la bdd
def obtener_conexion(incluir_db=True):

    # Especificamos los datos de la conexión
    config = {
        'host': os.getenv('DB_HOST'),
        'port': int(os.getenv('DB_PORT', 3306)),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD')
    }
    if incluir_db:
        config['database'] = DB_NAME
    return mysql.connector.connect(**config)

# Función para crear la bdd si no existe
def crear_bd():
    try:
        conn = obtener_conexion(incluir_db=False)
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME};")
        cursor.close()
        conn.close()
        print(f"Base de datos '{DB_NAME}' creada correctamente en RDS.")
    except Exception as e:
        print(f" Error al crear la base de datos en RDS: {e}")
        raise e

# Función para crear las tablas de la bdd
def crear_tablas():

    tables_sql = [
        "CREATE TABLE IF NOT EXISTS barrios (id_barrio INT AUTO_INCREMENT PRIMARY KEY, nombre VARCHAR(100) NOT NULL, poblacion INT NOT NULL, superficie_km2 DECIMAL(8,2) NOT NULL);",
        "CREATE TABLE IF NOT EXISTS empleados (id_empleado INT AUTO_INCREMENT PRIMARY KEY, nombre VARCHAR(100) NOT NULL, apellido VARCHAR(100) NOT NULL, dni VARCHAR(20) UNIQUE NOT NULL, cargo VARCHAR(50) NOT NULL, fecha_contrato DATE NOT NULL);",
        "CREATE TABLE IF NOT EXISTS tipo_residuos (id_tipo_residuo INT AUTO_INCREMENT PRIMARY KEY, nombre VARCHAR(50) NOT NULL, color_contenedor VARCHAR(30) NOT NULL);",
        "CREATE TABLE IF NOT EXISTS camiones (id_camion INT AUTO_INCREMENT PRIMARY KEY, matricula VARCHAR(20) UNIQUE NOT NULL, modelo VARCHAR(50) NOT NULL, capacidad_toneladas DECIMAL(5,2) NOT NULL, estado VARCHAR(30) NOT NULL);",
        "CREATE TABLE IF NOT EXISTS puntos_recogida (id_punto INT AUTO_INCREMENT PRIMARY KEY, id_barrio INT NOT NULL, direccion VARCHAR(200) NOT NULL, latitud DECIMAL(10,8) NOT NULL, longitud DECIMAL(11,8) NOT NULL, FOREIGN KEY (id_barrio) REFERENCES barrios(id_barrio) ON DELETE CASCADE);",
        "CREATE TABLE IF NOT EXISTS contenedores (id_contenedor INT AUTO_INCREMENT PRIMARY KEY, id_punto INT NOT NULL, id_tipo_residuo INT NOT NULL, capacidad INT NOT NULL, fecha_instalacion DATE NOT NULL, FOREIGN KEY (id_punto) REFERENCES puntos_recogida(id_punto) ON DELETE CASCADE, FOREIGN KEY (id_tipo_residuo) REFERENCES tipo_residuos(id_tipo_residuo) ON DELETE CASCADE);",
        "CREATE TABLE IF NOT EXISTS sensores_iot (id_sensor INT AUTO_INCREMENT PRIMARY KEY, id_contenedor INT NOT NULL, modelo VARCHAR(50) NOT NULL, porcentaje_bateria INT NOT NULL, estado VARCHAR(30) NOT NULL, FOREIGN KEY (id_contenedor) REFERENCES contenedores(id_contenedor) ON DELETE CASCADE);",
        "CREATE TABLE IF NOT EXISTS lecturas_sensores (id_lectura INT AUTO_INCREMENT PRIMARY KEY, id_sensor INT NOT NULL, porcentaje_lleno INT NOT NULL, temperatura DECIMAL(4,2) NOT NULL, timestamp_lectura DATETIME NOT NULL, FOREIGN KEY (id_sensor) REFERENCES sensores_iot(id_sensor) ON DELETE CASCADE);"
    ]

    try:
        conn = obtener_conexion(incluir_db=True)
        cursor = conn.cursor()
        for query in tables_sql:
            cursor.execute(query)
        conn.commit()
        cursor.close()
        conn.close()
        print("Tablas de CleanClan creadas en RDS.")
    except Exception as e:
        print(f" Error al crear tablas en RDS: {e}")
        raise e

# Función para poblar la bdd con datos de prueba
def poblar_datos_prueba():
    try:
        conn = obtener_conexion(incluir_db=True)
        cursor = conn.cursor()
        
        # Verificamos si ya hay empleados
        cursor.execute("SELECT COUNT(*) FROM empleados;")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO barrios (nombre, poblacion, superficie_km2) VALUES ('Centro', 35000, 4.5), ('Triana', 28000, 3.2);")
            cursor.execute("INSERT INTO empleados (nombre, apellido, dni, cargo, fecha_contrato) VALUES ('Carlos', 'Gómez', '12345678A', 'Conductor', '2022-01-15'), ('Lucía', 'Martín', '87654321B', 'Operario', '2023-03-10');")
            cursor.execute("INSERT INTO tipo_residuos (nombre, color_contenedor) VALUES ('Orgánico', 'Marrón'), ('Envases', 'Amarillo');")
            cursor.execute("INSERT INTO camiones (matricula, modelo, capacidad_toneladas, estado) VALUES ('1234-BCD', 'Volvo FE', 12.50, 'Operativo');")
            cursor.execute("INSERT INTO puntos_recogida (id_barrio, direccion, latitud, longitud) VALUES (1, 'Calle Sierpes 10', 37.3886, -5.9953);")
            cursor.execute("INSERT INTO contenedores (id_punto, id_tipo_residuo, capacidad, fecha_instalacion) VALUES (1, 1, 1000, '2023-01-01');")
            cursor.execute("INSERT INTO sensores_iot (id_contenedor, modelo, porcentaje_bateria, estado) VALUES (1, 'Sensor-v1', 85, 'Activo');")
            cursor.execute("INSERT INTO lecturas_sensores (id_sensor, porcentaje_lleno, temperatura, timestamp_lectura) VALUES (1, 92, 24.5, NOW());")
            conn.commit()
            print("Datos iniciales de prueba insertados en RDS.")
        else:
            print("La base de datos RDS ya tiene los datos de prueba.")
            
        cursor.close()
        conn.close()
    except Exception as e:
        print(f" Error al poblar datos iniciales: {e}")

# Ahora realizaremos las consultas json:

# Esta primera consulta mostrará todos los empleados de CleanClan
def consulta_empleados():
    conn = obtener_conexion(incluir_db=True)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id_empleado, nombre, apellido, cargo, fecha_contrato FROM empleados;")
    res = cursor.fetchall()
    cursor.close()
    conn.close()
    return json.dumps(res, indent=4, default=str)

# Esta segunda consulta devolverá los sensores con nivel de llenado por encima del 80%
def consulta_sensores_criticos():
    conn = obtener_conexion(incluir_db=True)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT s.id_sensor, s.modelo, l.porcentaje_lleno, l.temperatura, l.timestamp_lectura
        FROM sensores_iot s
        JOIN lecturas_sensores l ON s.id_sensor = l.id_sensor
        WHERE l.porcentaje_lleno > 80;
    """)
    res = cursor.fetchall()
    cursor.close()
    conn.close()
    return json.dumps(res, indent=4, default=str)

# Esta tercera consulta hará un Join de barrios, puntos de recogida y contenedores
def consulta_infraestructura_completa():
    conn = obtener_conexion(incluir_db=True)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT b.nombre AS barrio, p.direccion, tr.nombre AS tipo_residuo, c.capacidad
        FROM contenedores c
        JOIN puntos_recogida p ON c.id_punto = p.id_punto
        JOIN barrios b ON p.id_barrio = b.id_barrio
        JOIN tipo_residuos tr ON c.id_tipo_residuo = tr.id_tipo_residuo;
    """)
    res = cursor.fetchall()
    cursor.close()
    conn.close()
    return json.dumps(res, indent=4, default=str)