"""Food Review API package entrypoint."""

from food_review_api import api, core, products
from food_review_api.api.main import build_service_app
from food_review_api.main import main

__all__ = [
    "api",
    "build_service_app",
    "core",
    "main",
    "products",
]
