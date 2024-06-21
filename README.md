## Using Docker Secrets in Docker Compose for Production Deployment

### Overview

When deploying Docker containers in production, it's crucial to manage sensitive information such as passwords and configuration variables securely. Docker provides a feature called **secrets** to handle this securely. Secrets allow you to inject sensitive data into Docker containers without exposing it in the Dockerfile or docker-compose.yaml file.

### compose.prod.yaml Configuration
See the file `compose.prod.yaml` for the most current configuration

### Explanation

#### Flask Service (`flask_prod`)

- **Build and Command:** Configured to build from `./services/web` using `Dockerfile_prod` and run Gunicorn to serve the Flask application.
- **Ports:** Maps host port `5001` to container port `5000`.
- **Environment Variables:** Loaded from `.env_prod` file.
- **Dependencies:** Depends on `postgres_dev` service.

#### PostgreSQL Service (`postgres_prod`)

- **Image:** Uses the PostgreSQL 16.3 official Docker image.
- **Volumes:** Mounts a volume (`postgres_data_prod`) for persistent PostgreSQL data storage.

#### Secrets Section

- **Definitions:** Defines secrets for PostgreSQL and Flask to use:
  - `db_root_password`: Injects PostgreSQL root password into the PostgreSQL service.
  - `postgres_user`: Username for the PostgreSQL server
  - `postgres_password`: Password for the PostgreSQL user
  - `postgres_db`: Name of the PostgreSQL database for this project

#### Volumes

- **Persistence:** Creates a volume (`postgres_data_prod`) for persisting PostgreSQL data across container restarts.

### Creating Secret Files

- Before deploying the stack, create the following secret files in a `secrets` directory relative to your `docker-compose.prod.yaml` file:

    - **`postgres_root_password.txt`:**
       ```
       my_db_root_password
       ```

    - **`postgres_user.txt`:**
       ```
       hello_flask
       ```

    - **`postgres_password.txt`:**
       ```
       hello_flask
       ```

    - **`postgres_db.txt`:**
       ```
       hello_flask_prod
       ```

### Deploying the Stack

To deploy the stack in production:

1. **Build and Deploy:**
   ```sh
   docker compose -f compose.prod.yaml up -d
   ```
