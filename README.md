# docker-flask-postgres-template
An empty Flask Postgres full-stack template configured to be used with Pycharm Pro.

- The project has a debug configuration and a production configuration.
  - The `dev` config runs with `FLASK_DEBUG=1` for interactive debugger, and does not use secrets. Database storage is not persistent
  - The `prod` config runs with `FLASK_DEBUG=0` but uses secrets from docker to deploy with secure env passwords. Database storage is persistent using Docker Volumes

## Using PyCharm for debugging & docker controls
The PyCharm run configurations are present in this repositories `.idea` folder.
Steps to use them correctly with Docker/DockerCompose:
1. Open PyCharm and import the 4 configurations in the `.idea` folder (if they haven't automatically).
2. Create two `Remote Interpeters` with `docker compose` within PyCharm, one for `dev` and one for `prod`
   - Choose the corresponding docker compose file for each configuration
   - Choose the local Python interpreter to use
   - Assign the `dev` config to the PyCharm Run Configuration `FlaskDev`, and do the same for `prod` and its `FlaskProd` Run Configuration.
   - All corresponding images and PyCharm helper container should be created automatically.

- You could also use the `ComposeDev` & `ComposeProd` without any configuration to just control docker (no debugging possibilities) 
- If you don't have the PyCharm Pro edition, you could always rely on local development for debugging (Run Configuration not supplied):
  - Make a local interpreter in the `services/flask` folder (call it `local_venv_dev` for it to be ignored by docker, or change the corresponding `.dockerignore` file).
  - Install the required modules in the `local_venv_dev` (activate the environment, and execute `pip install -r requirements.txt`)
  - Develop/debug/test your code, and run the docker compose commands to check your results in the containers.


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
      
    - **`mail_smtp_server.txt`:**
       ```
       mail.domain.com
       ```      
      
    - **`mail_smtp_port.txt`:**
       ```
       465
       ```      
      
    - **`mail_sending_address.txt`:**
       ```
       info@test.com
       ```      
      
    - **`mail_sending_password.txt`:**
       ```
       coolandsecureemailpassword
       ```

### Deploying the Stack

To deploy the stack in production:

1. **Build and Deploy:**
   ```sh
   docker compose -f compose.prod.yaml up -d
   ```
