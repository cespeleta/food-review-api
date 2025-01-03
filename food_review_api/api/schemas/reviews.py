"""Food Review API reviews schema definitions."""

from pydantic import BaseModel

from food_review_api.products.schemas.review import Review


class ReviewsResponse(BaseModel):
    """Reviews API response model."""

    reviews: list[Review]
