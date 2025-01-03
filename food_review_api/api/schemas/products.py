"""Food Review API products schema definitions."""

from pydantic import BaseModel

from food_review_api.core.config.database import DatabaseConfig


class ProductsListResponse(BaseModel):
    """Reviews API response model."""

    available_products: list[str]


class ProductReviewsCountResponse(BaseModel):
    """Product Reviews Count API response model."""

    product_id: str
    number_of_reviews: int


class ProductsMetadataResponse(BaseModel):
    """Products Metadata API response model."""

    products: DatabaseConfig
