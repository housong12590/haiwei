import os


class Config(object):
    DEBUG = True

    SECRET_KEY = 'mwpcfnnwttcclwaf0r3bxwe3jr7epk74'

    MYSQL_HOST = os.environ.get('MYSQL_HOST') or '123.207.152.86'

    MYSQL_PORT = int(os.environ.get('MYSQL_PORT') or 3306)

    MYSQL_DB = os.environ.get('MYSQL_DB') or 'kx_ghost'

    MYSQL_USER = os.environ.get('MYSQL_USER') or 'root'

    MYSQL_PWD = os.environ.get('MYSQL_PASSWORD') or '123546'

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

    PROJECT_LIST = 'http://aegaeon.default.192.168.0.240.xip.io/products'

    # 开发环境k8s部署url
    DEPLOY_DEV_URL = 'http://aegaeon-dev.default.192.168.0.240.xip.io/products'

    # 生产环境k8s部署url
    DEPLOY_PRO_URL = 'http://aegaeon.default.192.168.0.240.xip.io/products'
