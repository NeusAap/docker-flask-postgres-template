from flask_login import UserMixin

from project import db, login_manager

from project.authentication.util import hash_pass


class Users(db.Model, UserMixin):
    __tablename__ = "Users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.LargeBinary)

    def __init__(self, **kwargs):
        for prop, value in kwargs.items():
            if hasattr(value, "__iter__") and not isinstance(value, str):
                value = value[0]

            if prop == "password":
                value = hash_pass(value)  # we need bytes here (not plain str)

            setattr(self, prop, value)

    def __repr__(self):
        return str(self.username)


@login_manager.user_loader
def user_loader(_id):
    return Users.query.filter_by(id=_id).first()


@login_manager.request_loader
def request_loader(request):
    username = request.form.get("username")
    user = Users.query.filter_by(username=username).first()
    return user if user else None
