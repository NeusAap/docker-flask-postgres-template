from . import blueprint, module_name
from ..util.routes_definition import create_blueprint_views_dynamically

create_blueprint_views_dynamically(blueprint, module_name)
