"""Food Review API reviews router definition."""

from logging import getLogger
from typing import Annotated

from fastapi import APIRouter, Depends

from food_review_api.api.dependencies import get_product_repository
from food_review_api.api.schemas.reviews import ReviewsResponse
from food_review_api.products.repository import ProductRepository

logger = getLogger(__name__)
router = APIRouter()


@router.get("", response_model=ReviewsResponse)
async def get_product_reviews(
    product_id: str,
    reviews_repository: Annotated[ProductRepository, Depends(get_product_repository)],
):
    """Get the reviews for a given product.

    Args:
        product_id (str): The `product_id` to get the reviews for.

    Returns:
        ReviewsResponse: A response containing the list of reviews for the given product.
    """
    logger.debug(f"Received request with product_id: {product_id}")
    return ReviewsResponse(reviews=reviews_repository.get(product_id).reviews)
