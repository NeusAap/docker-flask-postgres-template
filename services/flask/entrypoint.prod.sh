#!/usr/bin/env bash

set -e

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
    file_env "POSTGRES_USER"
    file_env "POSTGRES_PASSWORD"
    file_env "POSTGRES_DB"
    file_env "MAIL_SENDING_ADDRESS"
    file_env "MAIL_SENDING_PASSWORD"
    file_env "MAIL_SMTP_PORT"
    file_env "MAIL_SMTP_SERVER"

    if [ "$DATABASE" = "postgres" ]
    then
        echo "Waiting for postgres... HOST: $SQL_HOST, PORT: $SQL_PORT"

        while ! nc -z "$SQL_HOST" "$SQL_PORT"; do
          sleep 0.1
        done

        echo "PostgreSQL started"
    fi
fi

exec "$@"
