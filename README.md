# ToDo List API

### Build and Run the Application

To build and run the application using Docker Compose, follow these steps:

```bash
# Build the Docker containers
$ docker compose build

# Apply database migrations
$ make migrate

# Create a superuser for Django admin
$ make superuser

# Start the application
$ docker-compose up
```

The API will be available at `http://localhost:8000`.

## Running Tests

To run tests using pytest:

```bash
$ make test