from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object("project.config.Config")
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    def __init__(self, email):
        self.email = email


@app.route("/")
def hello_world():
    users_query = db.session.query(User).all()

    # Print or process your results
    output = [user.email for user in users_query]

    welcome_msg = str(output)

    # Return some response
    return render_template("home/welcome_page.html", welcome_msg=welcome_msg)

    # if app.debug:
    #     return jsonify(hello="DEBUG!")
    # return jsonify(hello="PROD!")
