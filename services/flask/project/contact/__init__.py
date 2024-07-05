from project import create_blueprint

module_name = __name__.split(".")[-1]
blueprint = create_blueprint(module_name)
