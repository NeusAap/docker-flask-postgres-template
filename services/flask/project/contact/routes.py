from flask import redirect, url_for, flash, request
from flask_mail import Message

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
        contact_us_form_data = ContactUsForm(**request.form)

        if not contact_us_form_data.validate_on_submit():
            message = "Error, could not validate form. Please try again."
            flash(message)
            return redirect(url_for(f"contact_blueprint.contact"))

        handle_form_submission_actions(contact_us_form_data)
        message = "Success, your message has been sent. We will contact you as soon as possible."
        flash(message)
        return redirect(url_for(f"contact_blueprint.contact"))


def handle_form_submission_actions(contact_us_form_data: ContactUsForm):
    insert_contact_form(contact_us_form_data)
    send_contact_form_mail(contact_us_form_data)


def insert_contact_form(contact_us_form_data: ContactUsForm):
    contact_form_entry = ContactUsModel(
        form_name=contact_us_form_data.your_name_field.data,
        form_email=contact_us_form_data.your_email_field.data,
        form_message=contact_us_form_data.your_message_field.data,
    )
    db.session.add(contact_form_entry)
    db.session.commit()


def send_contact_form_mail(contact_us_form_data: ContactUsForm):
    form_name = contact_us_form_data.your_name_field.data
    form_email = contact_us_form_data.your_email_field.data
    form_message = contact_us_form_data.your_message_field.data
    subject = f"Contact Form Submission by '{form_name}'"
    sender = "no-reply@mordekay.com"
    recip = "info@mordekay.com"
    body = (f"A form submission has been made by '{form_name}' from the email: '{form_email}'\n"
            f"The message of this form is:\n{form_message}")
    msg = Message(
        subject=subject, sender=sender, recipients=[recip], body=body
    )
    mailer_object = get_mail_object()
    mailer_object.send(msg)


create_blueprint_views_dynamically(blueprint, module_name)
