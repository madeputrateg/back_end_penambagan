# Flask Server (Dockerized)

This repository contains a Flask-based backend server that is designed to be run using **Docker Compose**. The application depends on environment variables defined in a `.env` file for database configuration.

---

## Prerequisites

Before running this project, make sure you have the following installed on your system:

- **Docker**
- **Docker Compose**
- **Git**

You can verify Docker and Docker Compose installation with:

```bash
docker --version
docker compose version

Environment Setup

Before running the application, you must create a .env file in the root directory of the project.

1. Create .env file
touch .env

2. Add the following variables to .env
DB_USER=
DB_NAME=
DB_HOST=
DB_PORT=
DB_PASSWORD=

3. Example .env configuration
DB_USER=postgres
DB_NAME=my_database
DB_HOST=db
DB_PORT=5432
DB_PASSWORD=secretpassword

Running the Application

Once the .env file is properly configured, run the following command in the root directory of the repository:

docker compose up --build


This command will:

Build the Docker images

Start the Flask server and its dependent services

Automatically load environment variables from .env