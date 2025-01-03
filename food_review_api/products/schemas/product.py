from pydantic import BaseModel, Field

from food_review_api.products.schemas.review import Review


class Product(BaseModel):
    """Product class."""

    product_id: str = Field(description="Unique identifier for the product")
    reviews: list[Review] = Field(
        description="List of reviews for the product", default_factory=list
    )
    number_of_reviews: int = Field(description="Number of reviews", ge=0)
