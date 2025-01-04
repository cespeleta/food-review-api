"""Food Review API main app definition."""

from fastapi import FastAPI

from food_review_api.api.exceptions import add_exception_handlers
from food_review_api.api.health import router as health_router
from food_review_api.api.lifespan import lifespan
from food_review_api.api.middelwares import add_middlewares
from food_review_api.api.v1.router import router as v1_router
from food_review_api.core.config.configuration import Configuration


def build_service_app() -> FastAPI:
    """Build service FastAPI app."""
    config = Configuration()
    app = FastAPI(
        title=config.api.title,
        description=config.api.description,
        openapi_url=config.api.openapi_url,
        version=config.version,
        lifespan=lifespan,
    )
    app.include_router(router=health_router)
    app.include_router(router=v1_router, prefix="/api/v1")
    add_exception_handlers(app=app)
    add_middlewares(app=app, config=config)
    return app
