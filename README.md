# Lazy Analysis System (LAS) - Challenge

## Deploy using Docker

To deploy this project using docker :

```bash
$ git clone https://github.com/salahalaoui/fastapi-celery-rabbitmq
```


Now move to the project root directory. The ``.env`` is committed to git history
just for the convenience of the developer reading this code: sensible environment variables should never be published in repositories.

```bash
$ mv fastapi-celery-rabbitmq
$ docker compose build
$ docker compose up
```

In order to use the analysis routes you should first authenticate at the top right of the application docs (``0.0.0.0:8080/docs``) in the button that reads ``Authorize``. Before that you need to create a new user with the POST ``register``

## Authentification

The API uses Bearer token from ``OAuth2PasswordBearer`` instead of a static api key, it's more secure because even it's compromised the token will expire and the user will have to ask for a new token.

## Stack

The docker-compose.yml is configured to create :
- an image of the application named ``app``,
- an image of PostgreSQL where we only store the user,
- an image of a celery worker,
- an image of RabbitMQ –``rabbit``– as celery broker
- an image of Redis v6.2 –``redis`` for celery backend
- an image of flower to monitor celery tasks at ``localhost:5556``.
- an image of pgadmin for PostgreSQL database administration at ``localhost:5050``

To see the application working sound and safe, please visit the URI ``localhost:8080/docs``

## Accepted files

The api uses the mime type to determine the nature and format of a file.

Current files accepted:
- ``application/vnd.openxmlformats-officedocument.wordprocessingml.document`` for ``.docx`` files
- ``text/plain`` for text-only data


## Asynchronous task performed

The celery task executed is word counter, because this task doesn't properly simulate a long task, the developper can add an environnement variable ``ADD_DELAY_TASK`` in secondes to make the task takes more time to execute.

