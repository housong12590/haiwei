import db_conf


class Config(object):
    DEBUG = True

    SECRET_KEY = 'akjs12ldf3ja12la1s23kldfjalsdjf'

    ORATOR_DATABASES = db_conf.DATABASES
