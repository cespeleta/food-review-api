"""Food Review API products package entrypoint."""

from food_review_api.products.repository import (
    ProductNotFoundInRepositoryError,
    ProductRepository,
    product_repository,
)

__all__ = [
    "ProductNotFoundInRepositoryError",
    "ProductRepository",
    "product_repository",
]
