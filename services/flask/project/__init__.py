from importlib import import_module

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


def register_extensions(_app):
    db.init_app(_app)
    login_manager.init_app(_app)


def register_blueprints(_app):
    for module_name in ("core", "authentication"):
        module = import_module("project.{}.routes".format(module_name))
        _app.register_blueprint(module.blueprint)


def create_app():
    _app = Flask(__name__)
    _app.config.from_object("project.config.Config")
    register_extensions(_app)
    register_blueprints(_app)
    Migrate(_app, db)
    return _app


db: SQLAlchemy = SQLAlchemy()
login_manager = LoginManager()
app = create_app()


if __name__ == "__main__":
    app.run()
