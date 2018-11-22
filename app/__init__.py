from flask import Flask, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_orator import Orator
from flask_login import LoginManager
from app.helper import utc2local, get_environs
from models import User
import os

db = Orator()
bootstrap = Bootstrap()
login_manager = LoginManager()


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'users.login'

    from .users import users as user_bp
    app.register_blueprint(user_bp, url_prefix='/users')
    from .docker import docker as docker_bp
    app.register_blueprint(docker_bp, url_prefix='/docker')
    # mysql 日志输出
    if config.DEBUG:
        mysql_log_output()

    template_filters = {
        'utc2local': utc2local,
        'get_environs': get_environs
    }
    app_redirect(app)
    app.jinja_env.filters.update(template_filters)
    configure_migrations(app)
    return app


def app_redirect(app):
    @app.route('/')
    def index():
        return redirect(url_for('docker.index'))


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


@login_manager.user_loader
def load_user(user_id):
    print("load_user  %s" % user_id)
    return User.find(user_id)
