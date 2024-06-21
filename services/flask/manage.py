from flask.cli import FlaskGroup

from project import app, db, User

"""

File to register new CLI commands through docker-compose.
Works for multiple different compose file setups. 

How to execute docker compose commands:
docker compose -f [COMPOSE FILE] exec [COMPOSE_SERVICE] python [THIS_FILENAME] [CLI_COMMAND]

Example usage:
docker compose -f compose.dev.yaml exec flask_dev python manage.py seed_db

"""

cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    db.session.add(User(email="test@domain.com"))
    db.session.commit()


if __name__ == "__main__":
    cli()
