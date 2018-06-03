from flask import Flask, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_orator import Orator
from app.helper import utc2local
import os

db = Orator()
bootstrap = Bootstrap()


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    bootstrap.init_app(app)

    from .build import build as build_bp
    app.register_blueprint(build_bp, url_prefix='/build')
    # mysql 日志输出
    if config.DEBUG:
        mysql_log_output()

    template_filters = {
        'utc2local': utc2local
    }
    app_redirect(app)
    app.jinja_env.filters.update(template_filters)
    configure_migrations(app)
    return app


def app_redirect(app):
    @app.route('/')
    def index():
        return redirect(url_for('build.projects'))


def configure_migrations(app):
    databases = app.config['ORATOR_DATABASES']
    with open('db_conf.py', 'w') as f:
        f.write('DATABASES = ' + str(databases))
    os.system('orator migrate -f -n -c db_conf.py')
    os.remove('db_conf.py')


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
