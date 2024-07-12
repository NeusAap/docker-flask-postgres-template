from flask_mail import Mail

mail = None


def init_mail(app):
    global mail
    mail = Mail(app)
    return mail


def get_mail_object():
    if mail is None:
        print("Mail object not yet initialized.")
        return None
    else:
        return mail
