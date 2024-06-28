import os


basedir = os.path.abspath(os.path.dirname(__file__))


def read_secret_file(file_path: str) -> str:
    """Reads the content of a secret file and returns it as a string."""
    try:
        with open(file_path, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        raise ValueError(f"Secret file {file_path} not found")

class Config(object):

    @staticmethod
    def get_database_uri() -> str:
        required_env_vars = ["SQL_HOST", "SQL_PORT"]
        required_secrets = ["POSTGRES_USER_FILE", "POSTGRES_PASSWORD_FILE", "POSTGRES_DB_FILE"]

        is_debug = os.getenv("FLASK_DEBUG") == "1"

        missing_vars = [var for var in required_env_vars if not os.getenv(var)]
        if missing_vars:
            raise ValueError(f"One or more required environment variables are missing: {', '.join(missing_vars)}")

        host = os.getenv("SQL_HOST")
        port = os.getenv("SQL_PORT")

        if is_debug:
            user = os.getenv("POSTGRES_USER")
            password = os.getenv("POSTGRES_PASSWORD")
            db_name = os.getenv("POSTGRES_DB")
            if not all([user, password, db_name]):
                raise ValueError("One or more required environment variables for database credentials are missing")
        else:
            missing_secrets = [var for var in required_secrets if not os.getenv(var)]
            if missing_secrets:
                raise ValueError(f"One or more required secret files are missing: {', '.join(missing_secrets)}")

            user_file = os.getenv("POSTGRES_USER_FILE")
            password_file = os.getenv("POSTGRES_PASSWORD_FILE")
            db_name_file = os.getenv("POSTGRES_DB_FILE")

            user = read_secret_file(user_file)
            password = read_secret_file(password_file)
            db_name = read_secret_file(db_name_file)

        return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"

    SQLALCHEMY_DATABASE_URI = get_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ASSETS_ROOT = os.getenv("ASSETS_ROOT", "/static")

