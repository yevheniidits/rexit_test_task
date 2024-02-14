# Test Project

This is a simple test project running via Docker Compose, based on FastAPI and PostgreSQL database.

## Getting Started

To start the application, follow these steps:

1. Clone this repository.
2. Navigate to the project directory.
3. Run the `bin/setup` script. This script will check for existing Docker and Docker Compose installations, install necessary requirements, and start the application.

## Environment Variables

You need to create a `.env` file to configure the environment variables. You can use the `env.sample` file provided in the repository as a reference.

Here's an example of the `.env` file:
```text
DEBUG=1
DATABASE_NAME=postgres
DATABASE_USER=postgres
DATABASE_PASSWORD=password
DATABASE_HOST=db
DATABASE_PORT=5432
```

Make sure to replace the values with your desired configuration.

## Docker Compose

The application runs in Docker containers orchestrated by Docker Compose. The `docker-compose.yml` file defines the services required for the application, including the FastAPI app and PostgreSQL database.

## Usage

Once the setup is complete and the application is running, you can access the FastAPI endpoints to interact with the application.
OpenAPI (Swagger) documentation available at `/swagger/`.

## Dependencies

The project relies on the following dependencies:

- FastAPI: A modern web framework for building APIs with Python.
- PostgreSQL: A powerful, open-source relational database system.
