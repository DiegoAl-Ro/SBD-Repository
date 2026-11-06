import redis

bd = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

print("LIMPIEZA COMPLETA DE BASE DE DATOS REDIS")

claves_antes = bd.dbsize()
bd.flushall()
claves_despues = bd.dbsize()

print(f"Claves antes del vaciado: {claves_antes}")
print(f"Claves después del vaciado: {claves_despues}")
print("Resultado: Base de datos Redis vaciada por completo.\n")