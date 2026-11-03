import redis

bd = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

bd.flushall()

# EJERCICIO 1: Crear Registros Clave Valor

print("-- EJERCICIO 1: Crear Registros Clave-Valor --")
print("Explicación: Registramos varios datos de contenedores de CleanClan usando bd.set().")

bd.set('contenedor:101:llenado', '85')
bd.set('contenedor:101:estado', 'critico')
bd.set('contenedor:102:llenado', '40')
bd.set('contenedor:102:estado', 'normal')
bd.set('contenedor:103:llenado', '95')

print("-> Resultado: Registros creados correctamente en la base de datos.\n")


# EJERCICIO 2: Obtener y mostrar el número de claves registradas

print("-- EJERCICIO 2: Obtener y mostrar el número de claves registradas --")
print("Explicación: Consultamos todas las claves con bd.keys() y mostramos la cantidad con len().")

claves = bd.keys()
print(f"-> Resultado: Número total de claves registradas = {len(claves)}\n")


# EJERCICIO 3: Obtener y mostrar un registro en base a una clave

print("-- EJERCICIO 3: Obtener y mostrar un registro en base a una clave --")
print("Explicación: Consultamos el valor asignado a la clave 'contenedor:101:llenado' con bd.get().")

clave_buscada = 'contenedor:101:llenado'
registro = bd.get(clave_buscada)

print(f"-> Resultado: El registro de '{clave_buscada}' tiene el valor: '{registro}%'\n")


# EJERCICIO 4: Actualizar el valor de una clave y mostrar el nuevo valor

print("-- EJERCICIO 4: Actualizar el valor de una clave y mostrar el nuevo valor --")
print("Explicación: Cambiamos el porcentaje de llenado del contenedor 101 de 85 a 90 con bd.set().")

clave_actualizar = 'contenedor:101:llenado'
valor_antes = bd.get(clave_actualizar)

bd.set(clave_actualizar, '90')

valor_despues = bd.get(clave_actualizar)

print(f"   [ANTES] El valor era: '{valor_antes}%'")
print(f"   [DESPUÉS] El nuevo valor es: '{valor_despues}%'")
print("-> Resultado: Clave actualizada con éxito.\n")


# EJERCICIO 5: Eliminar una clave-valor y mostrar la clave y el valor eliminado

print("-- EJERCICIO 5: Eliminar una clave-valor y mostrar la clave y el valor eliminado --")
print("Explicación: Guardamos el valor actual de la clave 'contenedor:103:llenado' y luego la eliminamos con bd.delete().")

clave_eliminar = 'contenedor:103:llenado'

valor_eliminado = bd.get(clave_eliminar)

print(f"   [ANTES] Claves registradas: {len(bd.keys())}")
print(f"   [ACCIONES] Eliminando la clave: '{clave_eliminar}' (Valor guardado: '{valor_eliminado}')")

bd.delete(clave_eliminar)

print(f"   [DESPUÉS] Claves registradas tras eliminar: {len(bd.keys())}")
print(f"-> Resultado: Se eliminó correctamente la clave '{clave_eliminar}' con el valor '{valor_eliminado}'.\n")


# EJERCICIO 6: Obtener y mostrar todas las claves guardadas

print("-- EJERCICIO 6: Obtener y mostrar todas las claves guardadas --")
print("Explicación: Obtenemos la lista completa de claves con bd.keys() y las mostramos una a una.")

todas_las_claves = bd.keys()

print("-> Claves encontradas en Redis:")
for clave in todas_las_claves:
    print(f"   - {clave}")
print()


# EJERCICIO 7: Obtener y mostrar todos los valores guardados

print("-- EJERCICIO 7: Obtener y mostrar todos los valores guardados --")
print("Explicación: Iteramos por todas las claves y extraemos su valor con bd.get().")

print("-> Valores guardados en Redis:")
for clave in bd.keys():
    valor = bd.get(clave)
    print(f"   - Clave: '{clave}' | Valor: '{valor}'")
print()

# EJERCICIO 8: Obtener y mostrar varios registros con una clave con un patrón en común usando



# EJERCICIO 9 Obtener y mostrar varios registros con una clave con un patrón en común usando



# EJERCICIO 10: Obtener y mostrar varios registros con una clave con un patrón en común usando



# EJERCICIO 11: Obtener y mostrar varios registros y filtrarlos por un valor en concreto



# EJERCICIO 12: Actualizar una serie de registros en base a un filtro



# EJERCICIO 13: Eliminar una serie de registros en base a un filtro



# EJERCICIO 14: Crear una estructura en JSON de array de los datos que vayais a almacenar



# EJERCICIO 15: Realizar un filtro por cada atributo de la estructura JSON anterior



# EJERCICIO 16: Crear una lista en Redis



# EJERCICIO 17: Obtener elementos de una lista con un filtro en concreto



# EJERCICIO 18: Crea datos con índices, definiendo un esquema de al menos tres campos



# EJERCICIO 19: Realiza una búsqueda con índices en base a un campo



# EJERCICIO 20: Realiza un group  by usando los índices