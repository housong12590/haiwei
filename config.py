import os


class Config(object):
    DEBUG = True

    SECRET_KEY = 'akjs12ldf3ja12la1s23kldfjalsdjf'

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:pss123546@123.207.152.86/haiwei?charset=utf8mb4'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MONGO_URI = 'mongodb://123.207.152.86:27017/haiwei'
