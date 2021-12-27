from fastapi import FastAPI

from app.config import settings

def create_app() -> FastAPI:
    app = FastAPI()

    from app.logging import configure_logging
    configure_logging()

    # do this before loading routes
    from app.celery_app.celery_utils import create_celery
    app.celery_app = create_celery()

    from app.views import analysis, auth
    app.include_router(analysis.router)
    app.include_router(auth.router)

    @app.get("/")
    async def root():
        return {"message": "Hello World"}

    return app