import json
import time

import redis
from pymysql import connect

# 连接redis 数据库
redis_client = redis.StrictRedis(host='127.0.0.1',port=6379,db=0)

# 数据库连接
mysql_client = connect(host='127.0.0.1',user='root',password='czh727657851',database='crawl_spider')
cursor = mysql_client.cursor()

i = 1
while True:
    print(i)
    time.sleep(1)
    # FIFO模式为 blpop，LIFO模式为 brpop，获取键值
    source,data = redis_client.blpop(["tieba_demo:items"])
    item = json.loads(data.decode())

    sql = """
    insert into blog(title,content) values (%s,%s)
    """
    params = [item['title'],item['content'],]
    cursor.execute(sql,params)
    mysql_client.commit()
    i += 1
