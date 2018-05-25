import db_conf


class Config(object):
    DEBUG = True

    SECRET_KEY = 'mwpcfnnwttcclwaf0r3bxwe3jr7epk74'

    MYSQL_HOST = '123.207.152.86'

    MYSQL_PORT = 3306

    MYSQL_DB = 'tx_ops'

    MYSQL_USER = 'root'

    MYSQL_PWD = 'pss123546'

    ORATOR_DATABASES = db_conf.DATABASES
