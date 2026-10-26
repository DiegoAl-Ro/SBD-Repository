import redis

bd = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# EJERCICIO 1: Crear Registros Clave Valor

print("--EJERCICIO 1: Crear Registros Clave-Valor--")

bd.set('contenedor:101:llenado', '85')
bd.set('contenedor:101:estado', 'critico')
bd.set('contenedor:102:llenado', '40')
bd.set('contenedor:102:estado', 'normal')
bd.set('contenedor:103:llenado', '95')

# EJERCICIO 2: Obtener y mostrar el número de claves registradas

print("--EJERCICIO 2: Obtener y mostrar el número de claves registradas--")

claves = bd.keys()

print(len(claves))

# EJERCICIO 3: Obtener y mostrar un registro en base a una clave

print("--EJERCICIO 3: Obtener y mostrar un registro en base a una clave--")

clave_buscada = 'contenedor:101:llenado'
registro = bd.get(clave_buscada)

print(f"La clave buscada es: '{registro}'\n")

# EJERCICIO 4: Actualizar el valor de una clave y mostrar el nuevo valor

print("--EJERCICIO 4: Actualizar el valor de una clave y mostrar el nuevo valor--")

bd.set('contenedor:101:llenado', '90')

bd.get('contenedor:101:llenado')

# EJERCICIO 5: Eliminar una clave-valor y mostrar la clave y el valor eliminado

print("--EJERCICIO 5: Eliminar una clave-valor y mostrar la clave y el valor eliminado--")

bd.delete('contenedor:103:llenado')

# EJERCICIO 6: Obtener y mostrar todas las claves guardadas

print("--EJERCICIO 6: Obtener y mostrar todas las claves guardadas--")

