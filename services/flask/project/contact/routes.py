import os

from flask import redirect, url_for, flash, request, current_app
from flask_mail import Message

import requests

from . import blueprint, module_name
from .forms import ContactUsForm
from .models import ContactUsModel
from .. import db
from ..init_mail import get_mail_object
from ..util.routes_definition import (
    create_blueprint_views_dynamically,
    create_route_handler,
)

urls = blueprint.module_subroute_urls
contact_us_url_subroute = urls[0]

def verify_recaptcha(token: str) -> tuple[bool, dict]:
    secret_key = current_app.config['RECAPTCHA_SECRET_KEY']
    verify_url = 'https://www.google.com/recaptcha/api/siteverify'

    if not secret_key:
        print("Secret key for recaptcha not set. Exiting.")
        exit(400)

    payload = {
        'secret': secret_key,
        'response': token
    }

    response = requests.post(verify_url, data=payload)
    result = response.json()

    # Define expected values
    valid_hostnames = ['mordekay.com', 'www.mordekay.com', '127.0.0.1', 'localhost']
    expected_action = 'submit_mordekay_contact_form'
    expected_minimum_score = 0.6

    # Check if the hostname matches any in the valid list
    if result.get('hostname') not in valid_hostnames:
        # Hostname mismatch, treat this as a failed validation
        return False, result

    # Check correct action
    if result.get('action') != expected_action:
        # Action mismatch, treat this as a failed validation
        return False, result

    # Check score value
    score = result.get('score', 0)
    if score < expected_minimum_score:
        return False, result

    return True, result  # All checks passed


@blueprint.route(f"/{contact_us_url_subroute}", methods=["GET", "POST"])
def contact():
    if request.method == "GET":
        contact_us_form = ContactUsForm()
        route_handler = create_route_handler(
            module_name=module_name,
            subroute_segment=contact_us_url_subroute,
            blueprint=blueprint,
            contact_us_form=contact_us_form,
        )
        return route_handler()
    else:
        contact_us_form_data: ContactUsForm = ContactUsForm(**request.form)

        if not contact_us_form_data.validate_on_submit():
            # Mapping of field names to user-friendly labels
            field_labels = {
                'your_name_field': 'Your Name',
                'your_email_field': 'Your Email',
                'your_message_field': 'Your Message',
                'recaptcha_response': 'reCAPTCHA'
            }

            # Retrieve specific errors
            error_messages = []
            for field, errors in contact_us_form_data.errors.items():
                # Get the friendly label or fallback to the field name if not found
                friendly_label = field_labels.get(field, field)
                for error in errors:
                    error_messages.append(f"{friendly_label}: {error}")

            # Create a complete error message
            message = "Error, could not validate form:\n " + "\n".join(error_messages)
            flash(message)
            return redirect(url_for(f"contact_blueprint.contact"))

        recaptcha_token = contact_us_form_data.recaptcha_response.data
        recaptcha_response: tuple[bool, dict] = verify_recaptcha(recaptcha_token)
        recaptcha_succeeded: bool = recaptcha_response[0]
        recaptcha_json_data: dict = recaptcha_response[1]

        if not recaptcha_succeeded:
            message = "Error, reCAPTCHA verification failed. Please try again."
            flash(message)
            insert_contact_form(contact_us_form_data, recaptcha_json_data)
            return redirect(url_for(f"contact_blueprint.contact"))

        insert_contact_form(contact_us_form_data, recaptcha_json_data)
        send_contact_form_mail(contact_us_form_data, recaptcha_json_data)
        message = "Success, your message has been sent. We will contact you as soon as possible."
        flash(message)
        return redirect(url_for(f"contact_blueprint.contact"))





def insert_contact_form(contact_us_form_data: ContactUsForm, recaptcha_json_data: dict):
    contact_form_entry = ContactUsModel(
        form_name=contact_us_form_data.your_name_field.data,
        form_email=contact_us_form_data.your_email_field.data,
        form_message=contact_us_form_data.your_message_field.data,
        form_recaptcha_json_data=recaptcha_json_data,
    )
    db.session.add(contact_form_entry)
    db.session.commit()


def send_contact_form_mail(contact_us_form_data: ContactUsForm, recaptcha_json_data: dict):
    form_name = contact_us_form_data.your_name_field.data
    form_email = contact_us_form_data.your_email_field.data
    form_message = contact_us_form_data.your_message_field.data
    subject = f"Contact Form Submission by '{form_name}'"
    sender = "no-reply@mordekay.com"
    recip = "info@mordekay.com"
    body = (f"A form submission has been made by '{form_name}' from the email: '{form_email}'\n"
            f"The message of this form is:\n{form_message}\n\n\n\n\n\n\n"
            f"The JSON data from this forms' reCAPTCHA request is: {recaptcha_json_data}")
    msg = Message(
        subject=subject, sender=sender, recipients=[recip], body=body
    )
    mailer_object = get_mail_object()
    mailer_object.send(msg)


create_blueprint_views_dynamically(blueprint, module_name)
