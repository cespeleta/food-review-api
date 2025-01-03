"""Food Review API logging utilities."""

from logging.config import dictConfig

from food_review_api.core.config import LoggingConfig


def configure_logging(logging_config: LoggingConfig):
    """Configure logging from configuration."""
    dict_config = logging_config.model_dump(exclude_none=True)
    dictConfig(dict_config)
