import redis

conexionRedis = redis.ConnectionPool(host='localhost', port=6379, db=0)
baseDatosRedis = redis.Redis(connection_pool=conexionRedis)

res1 = baseDatosRedis.lpush("usuarios:hobbies", "futbol:1")
res1 = baseDatosRedis.lpush("usuarios:hobbies", "tenis:2")
res1 = baseDatosRedis.lpush("usuarios:hobbies", "rugby:2")

res3 = baseDatosRedis.lrange("usuarios:hobbies", 0, -1)
print(res3)

res4 = baseDatosRedis.lrange("usuarios:hobbies")
print(res4)

res5 = baseDatosRedis.lrange("usuarios:hobbies")
print(res5)

res6 = baseDatosRedis.lrange("usuarios:hobbies", 0, -1)
print(res6)

baseDatosRedis.close()