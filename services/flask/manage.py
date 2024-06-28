import os

from flask.cli import FlaskGroup

from project import app, db
from project.authentication.models import Users

"""

File to register new CLI commands through docker-compose.
Works for multiple different compose file setups. 

How to execute docker compose commands:
docker compose -f [COMPOSE FILE] exec [COMPOSE_SERVICE] python [THIS_FILENAME] [CLI_COMMAND]

Example usage to seed the dev database:
docker compose -f compose.dev.yaml exec flask_dev python manage.py seed_db


Example usage to create prod database:
docker compose -f compose.prod.yaml exec flask_prod python manage.py create_db

"""

cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()
    print(f"Database created: {db.engine.url.database}")


@cli.command("create_dev_user")
def create_dev_user_db():
    password_str = "test"
    user_to_add = Users(username="dev", email="test@test.com", password=password_str)
    db.session.add(user_to_add)
    db.session.commit()
    print(f"Created dev user: {user_to_add.username} with password: {password_str}")


@cli.command("seed_db")
def seed_db():
    user_to_add = "test@domain.com"
    # db.session.add(user_to_add)
    # db.session.commit()
    print(f"Added user: {user_to_add}")


if __name__ == "__main__":
    cli()
