from flask import render_template, request
from jinja2 import TemplateNotFound

from . import blueprint
from .. import db
from ..authentication.models import Users


@blueprint.route("/")
# @login_required
def index():
    users_query = db.session.query(Users).all()

    registered_users: list[Users] = [user.username for user in users_query]

    return render_template(
        "home/home.html", segment="index", registered_users=registered_users
    )


@blueprint.route("/<path:template>")
# @login_required
def route_template(template):
    try:
        if not template.endswith(".html"):
            template += ".html"

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from project/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template("home/page-404.html"), 404

    except Exception as e:
        print(e)
        return render_template("home/page-500.html"), 500


def get_segment(_request):
    try:
        segment = _request.path.split("/")[-1]

        if segment == "":
            segment = "index"

        return segment

    except Exception as e:
        print(e)
        return None
