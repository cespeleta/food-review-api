"""Food Review API configuration package entrypoint."""

from food_review_api.api.main import build_service_app

__all__ = [
    "build_service_app",
]
