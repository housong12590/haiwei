import os


class Config(object):
    DEBUG = True

    SECRET_KEY = 'mwpcfnnwttcclwaf0r3bxwe3jr7epk74'

    MYSQL_HOST = os.environ.get('MYSQL_HOST') or '123.207.152.86'

    MYSQL_PORT = int(os.environ.get('MYSQL_PORT') or 3306)

    MYSQL_DB = os.environ.get('MYSQL_DB') or 'tx_ops_dev'

    MYSQL_USER = os.environ.get('MYSQL_USER') or 'root'

    MYSQL_PWD = os.environ.get('MYSQL_PASSWORD') or 'pss123546'

    ORATOR_DATABASES = {
        'default': 'mysql',
        'mysql': {
            'driver': 'mysql',
            'host': MYSQL_HOST,
            'port': int(MYSQL_PORT),
            'database': MYSQL_DB,
            'user': MYSQL_USER,
            'password': MYSQL_PWD,
            'log_queries': DEBUG
        }
    }

    project_list = 'http://192.168.0.240:30016/'

    dd = 'http://192.168.0.240:30016/products'
    data = {
        'id': '',
        'image': ''
    }
