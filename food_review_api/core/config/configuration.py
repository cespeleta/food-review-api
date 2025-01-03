"""Food Review API configuration class definition."""

import os
from importlib.metadata import version as package_version
from typing import ClassVar, Self

from pydantic import Field

from food_review_api.core.config.__base import BaseConfiguration
from food_review_api.core.config.api import ApiConfig
from food_review_api.core.config.database import DatabaseConfig
from food_review_api.core.config.logging import LoggingConfig

ENVIRONMENT = os.environ.get("MYT_ENVIRONMENT", "local")
SERVICE_NAME = os.environ.get("SERVICE_NAME", "food-review-api")


class Configuration(BaseConfiguration):
    """Application configuration settings."""

    environment: ClassVar[str] = ENVIRONMENT
    service_name: ClassVar[str] = SERVICE_NAME

    api: ApiConfig = Field(
        default_factory=ApiConfig.model_construct,
        title="API configuration",
        description=(
            "API configurable constants for API title, description OpenAPI endpoint "
            "and base URL."
        ),
    )
    logging: LoggingConfig = Field(
        default_factory=LoggingConfig.model_construct,
        title="Logging configuration",
        description=(
            "Python logger configuration options, following logging configuration "
            "dictionary schema."
        ),
    )
    database: DatabaseConfig = Field(
        default_factory=DatabaseConfig.model_construct,
        title="Database configuration",
        description=("Database configuration options, file with the reviews."),
    )

    @property
    def version(self: Self) -> str:
        """Get food review API package version."""
        return package_version("food_review_api")
