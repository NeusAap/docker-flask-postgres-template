#!/usr/bin/env bash

file_env() {
   local var="$1"
   local fileVar="${var}_FILE"
   local def="${2:-}"

   if [ "${!var:-}" ] && [ "${!fileVar:-}" ]; then
      echo >&2 "error: both $var and $fileVar are set (but are exclusive)"
      exit 1
   fi
   local val="$def"
   if [ "${!var:-}" ]; then
      val="${!var}"
   elif [ "${!fileVar:-}" ]; then
      val="$(< "${!fileVar}")"
   fi

   export "$var"="$val"
}

# Check if this is the Flask service container
if [ "$CONTAINER_ROLE" = "flask" ]; then
  echo "Setting up Flask environment..."
  file_env "MAIL_SENDING_ADDRESS"
  file_env "MAIL_SENDING_PASSWORD"
  file_env "MAIL_SMTP_PORT"
  file_env "MAIL_SMTP_SERVER"

  if [ "$DATABASE" = "postgres" ]
  then
      echo "Waiting for postgres..."

      while ! nc -z "$SQL_HOST" "$SQL_PORT"; do
        sleep 0.1
      done

      echo "PostgreSQL started"
  fi
fi

echo "Creating database"
python manage.py create_db

echo "Adding development user"
python manage.py create_dev_user

exec "$@"

