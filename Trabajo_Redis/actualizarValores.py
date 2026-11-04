import redis

conexionRedis = redis.ConnectionPool(host='localhost', port=6379, db=0)
baseDatosRedis = redis.Redis(connection_pool=conexionRedis)

print(baseDatosRedis.set('libro_1','El señor de los anillos'))
baseDatosRedis.set('libro_2', 'Hamlet')
baseDatosRedis.set('libro_3', 'Otelo')
baseDatosRedis.set('comic_1', 'Mortadelo y Filemón')
baseDatosRedis.set('comic_2', 'Superman')

baseDatosRedis.close()