from DBUtils.PooledDB import PooledDB
from config import Config

import pymysql

POOL = PooledDB(
    creator=pymysql,  # 使用链接数据库的模块
    maxusage=None,  # 一个链接最多被使用的次数，None表示无限制
    setsession=[],  # 开始会话前执行的命令
    ping=0,  # ping MySQL服务端,检查服务是否可用
    host=Config.MYSQL_HOST,
    port=Config.MYSQL_PORT,
    user=Config.MYSQL_USER,
    password=Config.MYSQL_PWD,
    database=Config.MYSQL_DB,
    charset='utf8mb4'
)


class SQLHelper(object):

    @staticmethod
    def execute(sql, args):
        conn = POOL.connection()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        result = cursor.execute(sql, args)
        cursor.commit()
        conn.close()
        return result

    @staticmethod
    def fetch_one(sql, args=None):
        if args is None:
            args = []
        conn = POOL.connection()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute(sql, args)
        result = cursor.fetchone()
        conn.close()
        return result

    @staticmethod
    def fetch_all(sql, args=None):
        if args is None:
            args = []
        conn = POOL.connection()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute(sql, args)
        result = cursor.fetchall()
        conn.close()
        return result
