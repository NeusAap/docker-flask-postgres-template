from importlib import import_module

from flask import Flask, Blueprint
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from project.init_mail import init_mail
from project.util.routes_definition import (
    get_all_website_routes,
    get_subroute,
    get_subroute_urls,
    get_subroute_labels,
)


def register_extensions(_app):
    db.init_app(_app)
    login_manager.init_app(_app)


def create_blueprint(module_name: str) -> Blueprint:
    """
    Creates a Flask Blueprint and sets up routes and labels for the module.

    Args:
        module_name (str): The name of the module.

    Returns:
        Blueprint: Configured Flask Blueprint for the module.
    """
    blueprint_name = module_name + "_blueprint"
    blueprint = Blueprint(blueprint_name, __name__, url_prefix=f"/{module_name}")

    module_routes: list[dict[str, str]] = get_subroute(module_name)
    module_subroute_urls = get_subroute_urls(module_routes)
    module_subroute_labels = get_subroute_labels(module_routes)

    # Store module-specific data in the blueprint for later use if needed
    blueprint.module_routes = module_routes
    blueprint.module_subroute_urls = module_subroute_urls
    blueprint.module_subroute_labels = module_subroute_labels

    return blueprint


def register_blueprints(_app):
    for module_name in ("core", "authentication", "services", "portfolio", "contact"):
        module = import_module("project.{}.routes".format(module_name))
        _app.register_blueprint(module.blueprint)


def create_app():
    _app = Flask(__name__)
    _app.config.from_object("project.config.Config")
    register_extensions(_app)
    register_blueprints(_app)
    init_mail(_app)
    Migrate(_app, db)
    return _app


db: SQLAlchemy = SQLAlchemy()
login_manager = LoginManager()
app = create_app()


# Define a context processor function
@app.context_processor
def inject_routes():
    all_routes = get_all_website_routes()

    # Filter out sections where all child elements have show=False
    filtered_routes = {}
    for section, links in all_routes["routes"].items():
        if any(link["show"] for link in links):
            filtered_routes[section] = links

    return dict(routes=filtered_routes)


if __name__ == "__main__":
    app.run()
