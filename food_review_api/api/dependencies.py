"""Food Review API dependencies function definitions."""

from food_review_api.core.config import Configuration
from food_review_api.products.repository import ProductRepository, product_repository


def fetch_configuration() -> Configuration:
    """Getter for application configuration.

    Returns:
        Configuration: The application configuration.
    """
    return Configuration()


def get_product_repository() -> ProductRepository:
    """Getter for product repository singleton."""
    return product_repository
