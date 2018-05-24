from flask import Flask
from config import Config
from flask_bootstrap import Bootstrap
from flask_orator import Orator

db = Orator()
bootstrap = Bootstrap()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    bootstrap.init_app(app)

    from .build import build as build_bp
    app.register_blueprint(build_bp, url_prefix='/build')
    # mysql 日志输出
    mysql_log_output()
    return app


def mysql_log_output():
    import logging
    logger = logging.getLogger('orator.connection.queries')
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        'It took %(elapsed_time)sms to execute the query %(query)s'
    )
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
