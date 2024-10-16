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


### Setting Up Docker Remote Context

To set up a remote Docker context:

1. **Create the Remote Docker Context**

    Define and create a new Docker context that connects to your remote Docker host via SSH. Replace `deployer` with your SSH username.

    ```sh
    docker context create mordekay-do \
      --description "Mordekay Docker" \
      --docker "host=ssh://deployer@REMOTE_IP"
    ```

2. **Use the Remote Context**

    Switch to the newly created Docker context for all Docker operations:

    ```sh
    docker context use mordekay-do
    ```

3. **Verify the Context**

    Ensure that the context has been set up correctly and is being used:

    ```sh
    docker context ls
    docker info
    ```

### Deploying the Stack

To deploy the stack in production:

1. **Prepare Secret Files**

    Ensure your secret files are securely stored on your server. Place them in `/home/deployer/dock_secrets/` and set strict file permissions.

    ```sh
    mkdir -p /home/deployer/dock_secrets
    cp /path/to/your/secrets/* /home/deployer/dock_secrets/
    sudo chmod 644 /home/deployer/dock_secrets/*
    sudo chown deployer:docker /home/deployer/dock_secrets/*
    ```
2. **Deploy the Stack**

    Use Docker Compose to deploy your services with the updated configuration:

    ```sh
    docker-compose --context mordekay-do -f compose.prod.yaml up -d
    ```
   
    Be wary that some servers might have SSH rate limiting applied to its `sshd` or firewall (`ufw` for example).
    Docker makes a huge amount of SSH requests in a short burst. You might want to update these limits.
    For DigitalOcean, their droplets are configured with an `ufw` rate limiter.
    ```sh
    sudo ufw status verbose
    sudo ufw delete limit 22/tcp
    sudo ufw limit 22/tcp
    -A ufw-before-input -p tcp --dport 22 -m conntrack --ctstate NEW -m limit --limit 5/minute --limit-burst 10 -j ACCEPT
    ```
    This removes old limits, creates new entry and accepts 5 requests per minute, with a max burst of 30. 


3. **Verify Deployment**

    Check the status of your containers to ensure they are running correctly and have access to the secrets:

    ```sh
    docker-compose --context mordekay-do -f compose.prod.yaml ps
    ```

### Securing server with SSL certificates (https)

1. **DNS settings for domain**
    Get a domain, and point the records to the hosting server.
    - Point the A record of the .DOMAIN.com to the IP4
    - Point the A record of the www.DOMAIN.com to the IP4
    - Remove the AAAA record for .DOMAIN.com (to disable IPv6, will be in the way for certificate creation)
    - Remove the AAAA record for www.DOMAIN.com (to disable IPv6, will be in the way for certificate creation)

2. **NGinX Config**
    Change the NGinX config file `./services/nginx/conf/nginx.conf` to match the new domain name 

3. **SSL via certbot in container**
   Creating certificates for the first time (`--dry-run` prevents request limits, but does not actually create certificate. Remove for production): 
   ```sh
    certbot certonly --webroot -w /var/www/certbot -d mordekay.com -d www.mordekay.com --text --agree-tos --email mats@mordekay.com --dry-run
   ```

4. **SSL renewal via certbot with SSH context**
Renewing existing certificates from local machine to remote over SSH context with docker:
   ```sh
   docker-compose --context mordekay-do -f compose.prod.yaml run --rm certbot renew --dry-run
   ```
