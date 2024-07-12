from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, EmailField, TextAreaField
from wtforms.validators import InputRequired, Email


class ContactUsForm(FlaskForm):
    your_name_field = StringField("YourNameField", id="your_name_field", validators=[])
    your_email_field = EmailField(
        "YourEmailField", id="your_email_field", validators=[InputRequired(), Email()]
    )
    your_message_field = TextAreaField(
        "YourMessageField", id="your_message_field", validators=[InputRequired()]
    )
