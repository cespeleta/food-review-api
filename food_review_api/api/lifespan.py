"""Food Review API lifespan definition."""

from contextlib import asynccontextmanager
from logging import getLogger

from fastapi import FastAPI

from food_review_api.core.config.configuration import Configuration
from food_review_api.products.repository import product_repository
from food_review_api.utils.logging import configure_logging

logger = getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    startup_event()
    yield
    shutdown_event()


def startup_event():
    """Lifespan function handling API startup and teardown logic."""
    logger.info("Application startup: API is starting up")
    config = Configuration()
    configure_logging(logging_config=config.logging)
    logger.info(
        "Service name: %s. Version: %s. Environment: %s",
        config.service_name,
        config.version,
        config.environment,
    )
    load_reviews(config)


def load_reviews(config: Configuration):
    """Load reviews from a CSV file.

    This function is part of the lifespan events and is called when the API is
    starting up. It loads the reviews from a CSV file, specified by the database
    configuration option, and adds them to the product repository.
    """
    logger.info("Loading reviews from a csv.")
    product_repository.load(config.database)
    logger.info(
        "Loaded %d reviews and %d products.",
        product_repository.review_count,
        product_repository.product_count,
    )


def shutdown_event():
    """Lifespan function handling API shutdown logic."""
    logger.info("Clearing review repository and shutting down.")
    product_repository.clear()
    logger.info("Application shutdown: API is shutting down")
