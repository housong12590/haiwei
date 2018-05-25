from DBUtils.PooledDB import PooledDB

import pymysql

POOL = PooledDB(
    creator=pymysql,  # 使用链接数据库的模块
    maxusage=None,  # 一个链接最多被使用的次数，None表示无限制
    setsession=[],  # 开始会话前执行的命令
    ping=0,  # ping MySQL服务端,检查服务是否可用
    host='123.207.152.86',
    port=3306,
    user='root',
    password='pss123546',
    database='tx_ops',
    charset='utf8mb4'
)


class SQLHelper(object):
    @staticmethod
    def insert(sql, args):
        conn = POOL.connection()
        cursor = conn.cursor()
        cursor.execute(sql, args)
        result = cursor.fetchall()
        conn.close()
        return result

    @staticmethod
    def fetch_one(sql, args):
        conn = POOL.connection()
        cursor = conn.cursor()
        cursor.execute(sql, args)
        result = cursor.fetchone()
        conn.close()
        return result

    @staticmethod
    def fetch_all(sql, args=None):
        if args is None:
            args = []
        conn = POOL.connection()
        cursor = conn.cursor()
        cursor.execute(sql, args)
        result = cursor.fetchall()
        conn.close()
        return result
