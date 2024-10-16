from project import db


class ContactUsModel(db.Model):
    __tablename__ = "contact_form_submissions"

    id = db.Column(db.Integer, primary_key=True)
    form_name = db.Column(db.String(256), unique=False, nullable=False)
    form_email = db.Column(db.String(256), unique=False, nullable=False)
    form_message = db.Column(db.Text, unique=False, nullable=False)
    form_recaptcha_json_data = db.Column(db.JSON, unique=False, nullable=True)

    def __init__(self, **kwargs):
        for prop, value in kwargs.items():
            if hasattr(value, "__iter__") and not isinstance(value, str) and not isinstance(value, dict):
                value = value[0]
            setattr(self, prop, value)

    def __repr__(self):
        return str(f"Form submission from: {self.form_name}")
