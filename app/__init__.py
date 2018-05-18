from flask import Flask
from config import Config
from flask_mongoengine import MongoEngine

db = MongoEngine()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    from .build import build as build_bp
    app.register_blueprint(build_bp, url_prefix='/build')

    return app
