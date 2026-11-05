import mysql.connector
import psycopg2

MYSQL_CONFIG = {'host': 'localhost', 'port': 3306, 'user': 'cleanuser', 'password': 'cleanpw', 'database': 'cleanclan_db'}
POSTGRES_CONFIG = {'host': 'localhost', 'port': 5432, 'user': 'cleanuser', 'password': 'cleanpw', 'dbname': 'cleanclan_db'}
MARIADB_CONFIG = {'host': 'localhost', 'port': 3307, 'user': 'cleanuser', 'password': 'cleanpw', 'database': 'cleanclan_db'}

SQL_TABLES_MYSQL = [
    "CREATE TABLE IF NOT EXISTS barrios (id_barrio INT AUTO_INCREMENT PRIMARY KEY, nombre VARCHAR(100) NOT NULL, poblacion INT NOT NULL, superficie_km2 DECIMAL(8,2) NOT NULL);",
    "CREATE TABLE IF NOT EXISTS empleados (id_empleado INT AUTO_INCREMENT PRIMARY KEY, nombre VARCHAR(100) NOT NULL, apellido VARCHAR(100) NOT NULL, dni VARCHAR(20) UNIQUE NOT NULL, cargo VARCHAR(50) NOT NULL, fecha_contrato DATE NOT NULL);",
    "CREATE TABLE IF NOT EXISTS tipo_residuos (id_tipo_residuo INT AUTO_INCREMENT PRIMARY KEY, nombre VARCHAR(50) NOT NULL, color_contenedor VARCHAR(30) NOT NULL);",
    "CREATE TABLE IF NOT EXISTS camiones (id_camion INT AUTO_INCREMENT PRIMARY KEY, matricula VARCHAR(20) UNIQUE NOT NULL, modelo VARCHAR(50) NOT NULL, capacidad_toneladas DECIMAL(5,2) NOT NULL, estado VARCHAR(30) NOT NULL);",
    "CREATE TABLE IF NOT EXISTS puntos_recogida (id_punto INT AUTO_INCREMENT PRIMARY KEY, id_barrio INT NOT NULL, direccion VARCHAR(200) NOT NULL, latitud DECIMAL(10,8) NOT NULL, longitud DECIMAL(11,8) NOT NULL, FOREIGN KEY (id_barrio) REFERENCES barrios(id_barrio) ON DELETE CASCADE);",
    "CREATE TABLE IF NOT EXISTS contenedores (id_contenedor INT AUTO_INCREMENT PRIMARY KEY, id_punto INT NOT NULL, id_tipo_residuo INT NOT NULL, capacidad INT NOT NULL, fecha_instalacion DATE NOT NULL, FOREIGN KEY (id_punto) REFERENCES puntos_recogida(id_punto) ON DELETE CASCADE, FOREIGN KEY (id_tipo_residuo) REFERENCES tipo_residuos(id_tipo_residuo) ON DELETE CASCADE);",
    "CREATE TABLE IF NOT EXISTS sensores_iot (id_sensor INT AUTO_INCREMENT PRIMARY KEY, id_contenedor INT NOT NULL, modelo VARCHAR(50) NOT NULL, porcentaje_bateria INT NOT NULL, estado VARCHAR(30) NOT NULL, FOREIGN KEY (id_contenedor) REFERENCES contenedores(id_contenedor) ON DELETE CASCADE);",
    "CREATE TABLE IF NOT EXISTS lecturas_sensores (id_lectura INT AUTO_INCREMENT PRIMARY KEY, id_sensor INT NOT NULL, porcentaje_lleno INT NOT NULL, temperatura DECIMAL(4,2) NOT NULL, timestamp_lectura DATETIME NOT NULL, FOREIGN KEY (id_sensor) REFERENCES sensores_iot(id_sensor) ON DELETE CASCADE);",
    "CREATE TABLE IF NOT EXISTS incidencias (id_incidencia INT AUTO_INCREMENT PRIMARY KEY, id_punto INT NOT NULL, fecha_reporte DATETIME NOT NULL, tipo VARCHAR(100) NOT NULL, estado_resolucion VARCHAR(50) NOT NULL, FOREIGN KEY (id_punto) REFERENCES puntos_recogida(id_punto) ON DELETE CASCADE);",
    "CREATE TABLE IF NOT EXISTS rutas_recogida (id_ruta INT AUTO_INCREMENT PRIMARY KEY, id_barrio INT NOT NULL, id_camion INT NOT NULL, id_empleado INT NOT NULL, fecha_ruta DATE NOT NULL, estado_ruta VARCHAR(30) NOT NULL, FOREIGN KEY (id_barrio) REFERENCES barrios(id_barrio) ON DELETE CASCADE, FOREIGN KEY (id_camion) REFERENCES camiones(id_camion) ON DELETE CASCADE, FOREIGN KEY (id_empleado) REFERENCES empleados(id_empleado) ON DELETE CASCADE);"
]

SQL_TABLES_POSTGRES = [
    sql.replace("INT AUTO_INCREMENT PRIMARY KEY", "SERIAL PRIMARY KEY").replace("DATETIME", "TIMESTAMP") 
    for sql in SQL_TABLES_MYSQL
]

def crear_tablas_mysql_mariadb(config, nombre_motor):
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        print(f"Creando tablas en {nombre_motor}...")
        for query in SQL_TABLES_MYSQL:
            cursor.execute(query)
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Tablas creadas correctamente en {nombre_motor}.")
    except Exception as e:
        print(f"Error en {nombre_motor}: {e}")

def crear_tablas_postgres(config):
    try:
        conn = psycopg2.connect(**config)
        cursor = conn.cursor()
        print("Creando tablas en PostgreSQL...")
        for query in SQL_TABLES_POSTGRES:
            cursor.execute(query)
        conn.commit()
        cursor.close()
        conn.close()
        print("Tablas creadas correctamente en PostgreSQL.")
    except Exception as e:
        print(f"Error en PostgreSQL: {e}")

if __name__ == "__main__":
    print("=== CREACIÓN DE LAS TABLAS EN BASE DE DATOS ===")
    crear_tablas_mysql_mariadb(MYSQL_CONFIG, "MySQL")
    crear_tablas_postgres(POSTGRES_CONFIG)
    crear_tablas_mysql_mariadb(MARIADB_CONFIG, "MariaDB")