import redis

conexionRedis = redis.ConnectionPool(host='localhost', port=6379, db=0)
baseDatosRedis = redis.Redis(connection_pool=conexionRedis)

print(baseDatosRedis.get('libro_1'))
print(baseDatosRedis.get('libro_2'))
print(baseDatosRedis.get('libro_3'))
print(baseDatosRedis.get('comic_1'))
print(baseDatosRedis.get('comic_2'))

baseDatosRedis.close()