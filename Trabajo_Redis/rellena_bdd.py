"""

Providers de Faker usados:

- facke.name(): Person(Nombres reales)
- fake.last_name(): Person (Apellidos)
- fake.ssn(): ssn / spanish_provider (DNI/Documentos)
- fake.job(): Job (Puestos de trabajo)
- fake.date_between(): Date_Time (Fechas pasadas)
- fake.street_address(): Address (Direcciones de calles)
- fake.latitude(): Geo (Coordenadas de latitud)
- fake.longitude(): Provider: Geo (Coordenadas de longitud)
- fake.license_plate(): Provider: Automotive (Matrículas de vehículos)
- fake.random_int(): Provider: Python (Números enteros aleatorios)

"""
import random
from datetime import datetime, timedelta
from faker import Faker
import mysql.connector
import psycopg2

fake = Faker('es_ES')

MYSQL_CONFIG = {'host': 'localhost', 'port': 3306, 'user': 'cleanuser', 'password': 'cleanpw', 'database': 'cleanclan_db'}
POSTGRES_CONFIG = {'host': 'localhost', 'port': 5432, 'user': 'cleanuser', 'password': 'cleanpw', 'dbname': 'cleanclan_db'}
MARIADB_CONFIG = {'host': 'localhost', 'port': 3307, 'user': 'cleanuser', 'password': 'cleanpw', 'database': 'cleanclan_db'}

def poblar_motor(config, nombre_motor, es_postgres=False):
    try:
        if es_postgres:
            conn = psycopg2.connect(**config)
        else:
            conn = mysql.connector.connect(**config)
            
        cursor = conn.cursor()
        print(f"Rellenando {nombre_motor}...")

        for _ in range(5):
            cursor.execute("INSERT INTO barrios (nombre, poblacion, superficie_km2) VALUES (%s, %s, %s)",
                           (f"Barrio {fake.first_name()}", fake.random_int(min=5000, max=50000), round(random.uniform(1.5, 10.0), 2)))

        for _ in range(10):
            cursor.execute("INSERT INTO empleados (nombre, apellido, dni, cargo, fecha_contrato) VALUES (%s, %s, %s, %s, %s)",
                           (fake.first_name(), fake.last_name(), fake.ssn(), random.choice(['Conductor', 'Mecánico', 'Inspector']), fake.date_between(start_date='-5y', end_date='today')))

        residuos = [('Orgánico', 'Marrón'), ('Envases', 'Amarillo'), ('Papel', 'Azul'), ('Vidrio', 'Verde')]
        for r in residuos:
            cursor.execute("INSERT INTO tipo_residuos (nombre, color_contenedor) VALUES (%s, %s)", r)

        for _ in range(5):
            cursor.execute("INSERT INTO camiones (matricula, modelo, capacidad_toneladas, estado) VALUES (%s, %s, %s, %s)",
                           (fake.license_plate(), f"Volvo-Evo{fake.random_int(1,5)}", round(random.uniform(8.0, 16.0), 2), 'Operativo'))

        for _ in range(10):
            cursor.execute("INSERT INTO puntos_recogida (id_barrio, direccion, latitud, longitud) VALUES (%s, %s, %s, %s)",
                           (fake.random_int(1, 5), fake.street_address(), float(fake.latitude()), float(fake.longitude())))

        for _ in range(15):
            cursor.execute("INSERT INTO contenedores (id_punto, id_tipo_residuo, capacidad, fecha_instalacion) VALUES (%s, %s, %s, %s)",
                           (fake.random_int(1, 10), fake.random_int(1, 4), 1000, fake.date_between(start_date='-2y', end_date='today')))

        for i in range(1, 16):
            cursor.execute("INSERT INTO sensores_iot (id_contenedor, modelo, porcentaje_bateria, estado) VALUES (%s, %s, %s, %s)",
                           (i, f"Sensor-v{fake.random_int(1,3)}", fake.random_int(20, 100), 'Activo'))

        for _ in range(30):
            cursor.execute("INSERT INTO lecturas_sensores (id_sensor, porcentaje_lleno, temperatura, timestamp_lectura) VALUES (%s, %s, %s, %s)",
                           (fake.random_int(1, 15), fake.random_int(0, 100), round(random.uniform(10.0, 35.0), 2), datetime.now() - timedelta(hours=random.randint(1, 72))))

        for _ in range(10):
            cursor.execute("INSERT INTO incidencias (id_punto, fecha_reporte, tipo, estado_resolucion) VALUES (%s, %s, %s, %s)",
                           (fake.random_int(1, 10), datetime.now() - timedelta(days=random.randint(1, 15)), random.choice(['Contenedor Lleno', 'Vandalismo', 'Tapa Rota']), random.choice(['Pendiente', 'En Proceso', 'Resuelto'])))

        for _ in range(10):
            cursor.execute("INSERT INTO rutas_recogida (id_barrio, id_camion, id_empleado, fecha_ruta, estado_ruta) VALUES (%s, %s, %s, %s, %s)",
                           (fake.random_int(1, 5), fake.random_int(1, 5), fake.random_int(1, 10), fake.date_between(start_date='-1m', end_date='today'), random.choice(['Completada', 'En Curso', 'Programada'])))

        conn.commit()
        cursor.close()
        conn.close()
        print(f"[✓] {nombre_motor} rellenado con éxito.")
    except Exception as e:
        print(f"Error llenando {nombre_motor}: {e}")

if __name__ == "__main__":
    print("=== POBLANDO BASES DE DATOS ===")
    poblar_motor(MYSQL_CONFIG, "MySQL")
    poblar_motor(POSTGRES_CONFIG, "PostgreSQL", es_postgres=True)
    poblar_motor(MARIADB_CONFIG, "MariaDB")