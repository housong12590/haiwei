import db_conf
import os


class Config(object):
    DEBUG = True

    SECRET_KEY = 'mwpcfnnwttcclwaf0r3bxwe3jr7epk74'

    MYSQL_HOST = os.environ.get('MYSQL_HOST')

    MYSQL_PORT = os.environ.get('MYSQL_PORT')

    MYSQL_DB = os.environ.get('MYSQL_DB')

    MYSQL_USER = os.environ.get('MYSQL_USER')

    MYSQL_PWD = os.environ.get('MYSQL_PASSWORD')

    ORATOR_DATABASES = db_conf.DATABASES


class DevConfig(Config):

    ORATOR_DATABASES = db_conf.DATABASES


class ProConfig(Config):
    DEBUG = False

    ORATOR_DATABASES = db_conf.DATABASES
