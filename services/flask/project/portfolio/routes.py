from . import blueprint, module_name
from ..util.routes_definition import create_blueprint_views_dynamically


# @blueprint.route("/motorsport-display")
# def motorsport_display():
#     return "test"


create_blueprint_views_dynamically(blueprint, module_name)
