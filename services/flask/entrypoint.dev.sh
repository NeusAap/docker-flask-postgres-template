#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z "$SQL_HOST" "$SQL_PORT"; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

echo "Creating database"
python manage.py create_db

echo "Adding development user"
python manage.py create_dev_user

exec "$@"

