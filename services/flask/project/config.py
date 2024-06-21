import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    @staticmethod
    def get_database_uri():
        required_vars = ["POSTGRES_USER", "POSTGRES_PASSWORD", "SQL_HOST", "SQL_PORT", "POSTGRES_DB"]
        missing_vars = []

        for var in required_vars:
            if not os.getenv(var):
                missing_vars.append(var)

        if missing_vars:
            raise ValueError(f"One or more required environment variables are missing: {', '.join(missing_vars)}")

        user = os.getenv("POSTGRES_USER")
        password = os.getenv("POSTGRES_PASSWORD")
        host = os.getenv("SQL_HOST")
        port = os.getenv("SQL_PORT")
        db_name = os.getenv("POSTGRES_DB")

        return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"

    SQLALCHEMY_DATABASE_URI = get_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False