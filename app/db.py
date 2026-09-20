from pymysqlpool.pool import Pool
# Параметры подключения
pool = Pool(
    host='db',
    port=3306,
    user='user',
    password='password',
    db='appDB',
    autocommit=True
)

# Создаём пул
pool.size=2
pool. maxsize=5
pool.pre_create_num=2, 
pool.init()
def get_pool_conn():
    return (pool.get_conn())

