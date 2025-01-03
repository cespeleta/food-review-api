"""Food Review API main module entrypoint definition."""

from logging import getLogger

from food_review_api.core.config import Configuration
from food_review_api.utils.logging import configure_logging

logger = getLogger(__name__)


def main():
    """Food Review API package main entrypoint."""
    config = Configuration()
    configure_logging(logging_config=config.logging)
    logger.info(
        "Service name: %s. Version: %s. Environment: %s",
        config.service_name,
        config.version,
        config.environment,
    )
