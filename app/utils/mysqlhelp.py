from DBUtils.PersistentDB import PersistentDB
import time

import pymysql

__pool = PersistentDB(
    creator=pymysql,  # 使用链接数据库的模块
    maxusage=None,  # 一个链接最多被使用的次数，None表示无限制
    setsession=[],  # 开始会话前执行的命令
    ping=0,  # ping MySQL服务端,检查服务是否可用
    closeable=False,  # conn.close()实际上被忽略，供下次使用，直到线程关闭，自动关闭链接，而等于True时，conn.close()真的被关闭
    threadlocal=None,  # 本线程独享值的对象，用于保存链接对象
    host='123.207.152.86',
    port=3306,
    user='root',
    password='pss123546',
    database='haiwei',
    charset='utf8mb4'
)


def exec_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(args, kwargs)
        end_time = time.time()
        print(end_time - start_time)
        return result

    return wrapper


@exec_time
def insert(sql, arg):
    conn = __pool.connection()
    cursor = conn.cursor()
    cursor.execute(sql, arg)
    result = cursor.fetchall()
    conn.close()
    return result


@exec_time
def fetchone(sql, arg):
    conn = __pool.connection()
    cursor = conn.cursor()
    cursor.execute(sql, arg)
    result = cursor.fetchall()
    conn.close()
    return result
