import redis

bd = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

bd.flushall()

print("\n(--- FUNCIONES DE REDIS 1 - 20 ---)\n")

print("-- EJERCICIO 1: Crear registros clave-valor --")
print("Explicación: Insertamos niveles de llenado y estados de contenedores usando bd.set().")

bd.set('contenedor:101:llenado', '85')
bd.set('contenedor:101:estado', 'critico')
bd.set('contenedor:102:llenado', '40')
bd.set('contenedor:102:estado', 'normal')
bd.set('contenedor:103:llenado', '95')
bd.set('contenedor:103:estado', 'critico')

print("\nRegistros creados correctamente.\n")

print("-- EJERCICIO 2: Obtener y mostrar el número de claves registradas --")
print("Explicación: Consultamos todas las claves con bd.keys() y contamos el total con len().")

claves = bd.keys()
print("\nEl número total de claves registradas es: {len(claves)}")

print("-- EJERCICIO 3: Obtener y mostrar un registro en base a una clave --")
print("Explicación: Consultamos el valor asignado a la clave 'contenedor:101:llenado' con bd.get().")

clave = 'contenedor:101:llenado'
registro = bd.get(clave)

print("\nEl registro es: '{registro}%'\n")

print("-- EJERCICIO 4: Actualizar el valor de una clave y mostrar el nuevo valor --")
print("Explicación: Cambiamos el nivel de llenado del contenedor 101 de 85 a 90 usando bd.set().")

print("\nLa clave que cambiaremos será esta: '{clave}'")
bd.set(clave, '90')
print("\nHa quedado así: '{clave}%'")

print("-- EJERCICIO 5: Eliminar una clave-valor y mostrar la clave y el valor eliminado --")
print("Explicación: Guardamos el valor actual de 'contenedor:103:llenado' y la eliminamos con bd.delete().")

claveBorrar = 'contenedor:103:estado'
valorBorrar = bd.get(claveBorrar)
print("\nLa clave que eliminaremos será la siguiente, '{claveBorrar}', con el valor: '{valorBorrar}%")
bd.delete(claveBorrar)
print("\nAhora la clave eliminada no aparecerá entre las otras: {key(bd.getkeys())}")