import db_conf
import os


class Config(object):
    DEBUG = True

    SECRET_KEY = 'mwpcfnnwttcclwaf0r3bxwe3jr7epk74'

    MYSQL_HOST = os.environ.get('MYSQL_HOST') or '123.207.152.86'

    MYSQL_PORT = int(os.environ.get('MYSQL_PORT') or 3306)

    MYSQL_DB = os.environ.get('MYSQL_DB') or 'tx_ops'

    MYSQL_USER = os.environ.get('MYSQL_USER') or 'root'

    MYSQL_PWD = os.environ.get('MYSQL_PASSWORD') or 'pss123546'

    ORATOR_DATABASES = db_conf.DATABASES


class DevConfig(Config):
    ORATOR_DATABASES = db_conf.DATABASES


class ProConfig(Config):
    DEBUG = False

    ORATOR_DATABASES = db_conf.DATABASES
