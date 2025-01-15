from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, EmailField, TextAreaField, HiddenField
from wtforms.validators import InputRequired, Email, DataRequired


class RecaptchaField(HiddenField):
    def process_formdata(self, valuelist):
        # Ensure only non-empty values are processed
        if valuelist:
            # Filter out empty values, and only take the first valid token
            self.data = next((val for val in valuelist if val), None)


class ContactUsForm(FlaskForm):
    your_name_field = StringField("YourNameField", id="your_name_field", validators=[InputRequired()])
    your_email_field = EmailField(
        "YourEmailField", id="your_email_field", validators=[InputRequired(), Email()]
    )
    your_message_field = TextAreaField(
        "YourMessageField", id="your_message_field", validators=[InputRequired()]
    )
    recaptcha_response = RecaptchaField('g-recaptcha-response', validators=[DataRequired()])