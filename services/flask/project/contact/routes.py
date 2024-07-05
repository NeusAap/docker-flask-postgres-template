from flask import request, redirect, url_for, flash

from . import blueprint, module_name
from ..util.routes_definition import create_blueprint_views_dynamically, create_route_handler

urls = blueprint.module_subroute_urls
contact_us_url_subroute = urls[0]


@blueprint.route(f"/{contact_us_url_subroute}", methods=['POST'])
def contact():
    if request.method == 'POST':
        # Flash the message
        message = "Error in Form submission"
        flash(message)
        return redirect(url_for(f'contact_blueprint.contact'))


create_blueprint_views_dynamically(blueprint, module_name)
