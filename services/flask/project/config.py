import os
import random
import string
from distutils.util import strtobool


basedir = os.path.abspath(os.path.dirname(__file__))


def read_secret_file(file_path: str) -> str:
    """Reads the content of a secret file and returns it as a string."""
    try:
        with open(file_path, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        raise ValueError(f"Secret file {file_path} not found")


def str_to_bool(s: str) -> bool:
    return bool(strtobool(s))


class Config(object):
    @staticmethod
    def get_database_uri() -> str:
        required_env_vars = ["SQL_HOST", "SQL_PORT", "MAIL_USE_TLS", "MAIL_USE_SSL"]
        required_secrets = [
            "POSTGRES_USER_FILE",
            "POSTGRES_PASSWORD_FILE",
            "POSTGRES_DB_FILE",
            "MAIL_SENDING_ADDRESS_FILE",
            "MAIL_SENDING_PASSWORD_FILE",
            "MAIL_SMTP_PORT_FILE",
            "MAIL_SMTP_SERVER_FILE",
        ]

        is_debug = os.getenv("FLASK_DEBUG") == "1"

        missing_vars = [var for var in required_env_vars if not os.getenv(var)]
        if missing_vars:
            raise ValueError(
                f"One or more required environment variables are missing: {', '.join(missing_vars)}"
            )

        sql_host = os.getenv("SQL_HOST")
        sql_port = os.getenv("SQL_PORT")

        if is_debug:
            user = os.getenv("POSTGRES_USER")
            password = os.getenv("POSTGRES_PASSWORD")
            db_name = os.getenv("POSTGRES_DB")
            if not all([user, password, db_name]):
                raise ValueError(
                    "One or more required environment variables for database credentials are missing"
                )
        else:
            missing_secrets = [var for var in required_secrets if not os.getenv(var)]
            if missing_secrets:
                raise ValueError(
                    f"One or more required secret files are missing: {', '.join(missing_secrets)}"
                )

            user_file = os.getenv("POSTGRES_USER_FILE")
            password_file = os.getenv("POSTGRES_PASSWORD_FILE")
            db_name_file = os.getenv("POSTGRES_DB_FILE")

            user = read_secret_file(user_file)
            password = read_secret_file(password_file)
            db_name = read_secret_file(db_name_file)

        return f"postgresql://{user}:{password}@{sql_host}:{sql_port}/{db_name}"

    SQLALCHEMY_DATABASE_URI = get_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ASSETS_ROOT = os.getenv("ASSETS_ROOT", "/static")

    # Mail setup
    _mail_use_tls = os.getenv("MAIL_USE_TLS")
    _mail_use_ssl = os.getenv("MAIL_USE_SSL")
    _mail_sending_address_file = os.getenv("MAIL_SENDING_ADDRESS_FILE")
    _mail_sending_password_file = os.getenv("MAIL_SENDING_PASSWORD_FILE")
    _mail_smtp_port_file = os.getenv("MAIL_SMTP_PORT_FILE")
    _mail_smtp_server_file = os.getenv("MAIL_SMTP_SERVER_FILE")

    MAIL_SERVER = read_secret_file(_mail_smtp_server_file)
    MAIL_PORT = read_secret_file(_mail_smtp_port_file)
    MAIL_USERNAME = read_secret_file(_mail_sending_address_file)
    MAIL_PASSWORD = read_secret_file(_mail_sending_password_file)
    MAIL_USE_TLS = str_to_bool(_mail_use_tls)
    MAIL_USE_SSL = str_to_bool(_mail_use_ssl)

    SECRET_KEY = os.getenv("SECRET_KEY", None)
    if not SECRET_KEY:
        SECRET_KEY = "".join(random.choice(string.ascii_lowercase) for i in range(32))
