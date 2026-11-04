import redis

conexionRedis = redis.ConnectionPool(host='localhost', port=6379, db=0)
baseDatosRedis = redis.Redis(connection_pool=conexionRedis)

print("Los Libros:")
for clave in baseDatosRedis.scan_iter('libro*'):
    print(clave)

baseDatosRedis.close()