# FastAPI + Celery for Async tasks

## Deploy using Docker

To deploy this project using docker :

```bash
$ git clone https://github.com/salahalaoui/fastapi-celery-rabbitmq
```


Now move to the project root directory. The ``.env`` is commited to git history
just for the convenience of the developer reading this code: environnement variables should never be published in repositories.

```bash
$ mv fastapi-celery-rabbitmq
$ docker compose build
$ docker compose up
```

The docker-compose.yml is configured to create an image of the application named ``app``, an image of PostgreSQL, RabbitMQ –``rabbit``– an image of Redis v6.2 –``redis`` and Flower. To see the application working sound and safe, please visit the URI ``localhost:8080/docs``

In order to use the analysis routes you should first authenticate at the top right of the application docs (``0.0.0.0:8080/docs``) in the button that reads ``Authorize``. Before that you need to create a new user with the POST ``register``


