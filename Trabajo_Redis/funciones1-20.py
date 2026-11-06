import time
import json
import redis
from redis.commands.json.path import Path
from redis.commands.search.field import TagField, NumericField, TextField
from redis.commands.search.query import Query
from redis.commands.search.aggregation import AggregateRequest, Desc

bd = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

bd.flushall()

# --------------------------------------------------
print("EJERCICIO 1: Crear registros clave-valor")
print("Explicación: Insertamos niveles de llenado y estados de contenedores usando bd.set().")

bd.set('contenedor:101:llenado', '85')
bd.set('contenedor:101:estado', 'critico')
bd.set('contenedor:102:llenado', '40')
bd.set('contenedor:102:estado', 'normal')
bd.set('contenedor:103:llenado', '95')
bd.set('contenedor:103:estado', 'critico')

print("\nRegistros creados correctamente.\n")

# --------------------------------------------------
print("EJERCICIO 2: Obtener y mostrar el número de claves registradas")
print("Explicación: Consultamos todas las claves con bd.keys() y contamos el total con len().")

claves = bd.keys()
print(f"\nEl número total de claves registradas es: {len(claves)}\n")

# --------------------------------------------------
print("EJERCICIO 3: Obtener y mostrar un registro en base a una clave")
print("Explicación: Consultamos el valor asignado a la clave 'contenedor:101:llenado' con bd.get().")

claveEspecifica = 'contenedor:101:llenado'
registro = bd.get(claveEspecifica)

print(f"\nEl registro de '{claveEspecifica}' es: '{registro}%'\n")

# --------------------------------------------------
print("EJERCICIO 4: Actualizar el valor de una clave y mostrar el nuevo valor")
print("Explicación: Cambiamos el nivel de llenado del contenedor 101 de 85 a 90 usando bd.set().")

print(f"\n Antes la clave '{claveEspecifica}' tenía el valor: {bd.get(claveEspecifica)}%")
bd.set(claveEspecifica, '90')
print(f"Después ha quedado así: '{claveEspecifica}' = {bd.get(claveEspecifica)}%\n")

# --------------------------------------------------
print("EJERCICIO 5: Eliminar una clave-valor y mostrar la clave y el valor eliminado")
print("Explicación: Guardamos el valor actual de 'contenedor:103:estado' y la eliminamos con bd.delete().")

claveBorrar = 'contenedor:103:estado'
valorBorrar = bd.get(claveBorrar)
print(f"\n Antes la clave '{claveBorrar}' tenía el valor: '{valorBorrar}'")
bd.delete(claveBorrar)
print(f"Después la clave '{claveBorrar}' ha sido eliminada (0 = No existe): {bd.exists(claveBorrar)}\n")

# --------------------------------------------------
print("EJERCICIO 6: Obtener y mostrar todas las claves guardadas")
print("Explicación: Recorremos las claves obtenidas con bd.keys() mediante un bucle for.")

todasClaves = bd.keys()
print("\nLas claves guardadas son:")
for c in todasClaves:
    print(c)
print()

# --------------------------------------------------
print("EJERCICIO 7: Obtener y mostrar todos los valores guardados")
print("Explicación: Obtenemos cada clave y extraemos su contenido ejecutando bd.get(clave).")

for c in todasClaves:
    if bd.exists(c):
        valor = bd.get(c)
        print(f"Clave: {c} | Valor: {valor}")
print()

# --------------------------------------------------
print("EJERCICIO 8: Filtrar claves usando el comodín * (coincidencia múltiple)")
print("Explicación: Buscamos todas las claves de tipo llenado usando el patrón 'contenedor:*:llenado'.")

clavesFiltradas = bd.keys('contenedor:*:llenado')
print("\nLas claves filtradas son:")
for c in clavesFiltradas:
    print(c)
print()

# --------------------------------------------------
print("EJERCICIO 9: Filtrar claves usando corchetes [] (rango de caracteres)")
print("Explicación: Filtramos únicamente los contenedores cuyo ID sea 101 o 102 usando 'contenedor:10[12]:llenado'.")

clavesFiltradas2 = bd.keys('contenedor:10[12]:llenado')
print("\nAquí están las claves que coinciden con 'contenedor:10[12]:llenado':")
for c in clavesFiltradas2:
    print(c)
print()

# --------------------------------------------------
print("EJERCICIO 10: Filtrar claves usando ? (un único carácter comodín)")
print("Explicación: Usamos 'contenedor:10?:llenado' para emparejar cualquier carácter individual en la tercera posición del ID.")

clavesEspecificas = bd.keys('contenedor:10?:llenado')
print("\nLas claves que coinciden con 'contenedor:10?:llenado' son:")
for c in clavesEspecificas:
    print(c)
print()

# --------------------------------------------------
print("EJERCICIO 11: Filtrar registros por valor específico en código")
print("Explicación: Buscamos contenedores cuyo nivel de llenado sea estrictamente mayor al 50%.")

print("\nContenedores con nivel de llenado > 50%:")
for c in bd.keys('contenedor:*:llenado'):
    valor = int(bd.get(c))
    if valor > 50:
        print(f"- {c} = {valor}%")
print()

# --------------------------------------------------
print("EJERCICIO 12: Actualizar una serie de registros según filtro (Incremento)")
print("Explicación: Incrementamos en +5% el llenado de todos los contenedores registrados usando bd.incrby().")

clavesInc = bd.keys('contenedor:*:llenado')
print("\nAntes, valores:")
for c in clavesInc:
    print(f"- {c} = {bd.get(c)}%")

for c in clavesInc:
    bd.incrby(c, 5)

print("\nDespués, valores actualizados (+5%):")
for c in clavesInc:
    print(f"   - {c} = {bd.get(c)}%")
print("-> Efecto: Todos los niveles de llenado aumentaron en 5 unidades.\n")

# --------------------------------------------------
print("EJERCICIO 13: Eliminar una serie de registros según filtro")
print("Explicación: Eliminamos todas las claves que almacenen estados de contenedores ('contenedor:*:estado').")

claves_estado = bd.keys('contenedor:*:estado')
print(f"\n Antes las claves de estado a borrar eran: {claves_estado}")
if claves_estado:
    bd.delete(*claves_estado)
print(f"Después las claves de estado restantes son: {bd.keys('contenedor:*:estado')}\n")

# --------------------------------------------------
print("EJERCICIO 14: Crear estructura JSON de array de datos")
print("Explicación: Almacenamos una lista de objetos JSON con información detallada de la flota de camiones de CleanClan.")

camiones_json = [
    {"id_camion": 1, "matricula": "1234-BCD", "modelo": "Volvo FE", "capacidad": 12.5, "estado": "Operativo"},
    {"id_camion": 2, "matricula": "5678-FGH", "modelo": "Mercedes Econic", "capacidad": 15.0, "estado": "Mantenimiento"},
    {"id_camion": 3, "matricula": "9012-JKL", "modelo": "Scania L-Series", "capacidad": 10.0, "estado": "Operativo"},
    {"id_camion": 4, "matricula": "3456-MNP", "modelo": "MAN TGM", "capacidad": 18.0, "estado": "Operativo"}
]

bd.json().set('cleanclan:camiones', Path.root_path(), camiones_json)
print("\nDocumento JSON guardado bajo la clave 'cleanclan:camiones'.\n")

# --------------------------------------------------
print("EJERCICIO 15: Filtrado por cada atributo de la estructura JSON")
print("Explicación: Consultamos los elementos del array JSON filtrando en Python por cada uno de sus 5 atributos.")

datos_camiones = bd.json().get('cleanclan:camiones')

print("1. Filtro por 'id_camion' (id_camion == 2):")
print(f"   {[c for c in datos_camiones if c['id_camion'] == 2]}")

print("2. Filtro por 'matricula' (matricula == '1234-BCD'):")
print(f"   {[c for c in datos_camiones if c['matricula'] == '1234-BCD']}")

print("3. Filtro por 'modelo' (modelo contiene 'Volvo'):")
print(f"   {[c for c in datos_camiones if 'Volvo' in c['modelo']]}")

print("4. Filtro por 'capacidad' (capacidad >= 15.0 toneladas):")
print(f"   {[c for c in datos_camiones if c['capacidad'] >= 15.0]}")

print("5. Filtro por 'estado' (estado == 'Operativo'):")
print(f"   {[c for c in datos_camiones if c['estado'] == 'Operativo']}")
print("\nSe han aplicado filtros individuales sobre id_camion, matricula, modelo, capacidad y estado.\n")

# --------------------------------------------------
print("EJERCICIO 16: Crear una lista en Redis (Estructura LIST)")
print("Explicación: Creamos una cola de avisos de incidencias urgentes utilizando bd.rpush().")

lista_incidencias = 'cleanclan:cola_incidencias'
bd.rpush(lista_incidencias, "INC-001: Contenedor lleno en Barrio Centro")
bd.rpush(lista_incidencias, "INC-002: Tapa rota en Barrio Triana")
bd.rpush(lista_incidencias, "INC-003: Contenedor quemado en Barrio Nervión")
bd.rpush(lista_incidencias, "INC-004: Fuga de líquidos en Barrio Centro")
print(f"Lista '{lista_incidencias}' creada correctamente con {bd.llen(lista_incidencias)} elementos.\n")

# --------------------------------------------------
print("EJERCICIO 17: Obtener elementos de una lista con un filtro")
print("Explicación: Filtramos los elementos de la lista que corresponden únicamente al 'Barrio Centro'.")

todos_avisos = bd.lrange(lista_incidencias, 0, -1)
avisos_centro = [inc for inc in todos_avisos if "Barrio Centro" in inc]

print("Incidencias filtradas para 'Barrio Centro':")
for inc in avisos_centro:
    print(f" - {inc}")
print()

# --------------------------------------------------
print("EJERCICIO 18: Crear datos con índices (Esquema de 3 campos)")
print("Explicación: Guardamos HASHES de sensores IoT y creamos un índice secundario con RediSearch sobre 3 campos.")

bd.hset('sensor:1', mapping={'modelo': 'Sensor-v1', 'bateria': 85, 'estado': 'Activo'})
bd.hset('sensor:2', mapping={'modelo': 'Sensor-v2', 'bateria': 15, 'estado': 'Critico'})
bd.hset('sensor:3', mapping={'modelo': 'Sensor-v1', 'bateria': 92, 'estado': 'Activo'})
bd.hset('sensor:4', mapping={'modelo': 'Sensor-v3', 'bateria': 45, 'estado': 'Inactivo'})
bd.hset('sensor:5', mapping={'modelo': 'Sensor-v2', 'bateria': 10, 'estado': 'Critico'})

nombre_indice = 'idx:sensores'
esquema = (
    TextField('modelo', as_name='modelo'),
    NumericField('bateria', as_name='bateria'),
    TagField('estado', as_name='estado')
)

try:
    bd.ft(nombre_indice).dropindex(delete_documents=False)
except:
    pass

bd.ft(nombre_indice).create_index(
    esquema,
    definition=redis.commands.search.indexDefinition.IndexDefinition(prefix=['sensor:']) if hasattr(redis.commands.search, 'indexDefinition') else None
)

print("Sincronizando índice RediSearch...")
time.sleep(1)
print("Índice creado con éxito.\n")

# --------------------------------------------------
print("EJERCICIO 19: Búsqueda con índices en base a un campo")
print("Explicación: Ejecutamos una búsqueda indexada para encontrar sensores con batería menor o igual a 20% (@bateria:[0 20]).")

query_bateria = Query('@bateria:[0 20]')
resultados = bd.ft(nombre_indice).search(query_bateria)

print(f"Se han encontrado {resultados.total} sensores en estado de batería crítica:")
for doc in resultados.docs:
    print(f"- ID: {doc.id} | Modelo: {doc.modelo} | Batería: {doc.bateria}% | Estado: {doc.estado}")
print()

# --------------------------------------------------
print("EJERCICIO 20: Realizar un GROUP BY usando los índices")
print("Explicación: Agrupamos los sensores por su campo 'estado' y contamos cuántos sensores hay en cada estado.")

request = AggregateRequest('*').group_by('@estado').sort_by(Desc('@estado'))
res_agrupado = bd.ft(nombre_indice).aggregate(request)

print("Conteo agregados (GROUP BY estado):")
for fila in res_agrupado.rows:
    # Convertimos la estructura de la fila en un diccionario flexible
    datos_fila = {fila[i]: fila[i+1] for i in range(0, len(fila), 2)}
    
    estado_val = datos_fila.get('estado', 'Desconocido')
    conteo_val = datos_fila.get('__count', 0)
    print(f" - Estado: '{estado_val}' | Cantidad de sensores: {conteo_val}")