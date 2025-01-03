"""Food Review API products router definition."""

from logging import getLogger
from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, Query

from food_review_api.api.dependencies import fetch_configuration, get_product_repository
from food_review_api.api.schemas.products import (
    ProductReviewsCountResponse,
    ProductsListResponse,
    ProductsMetadataResponse,
)
from food_review_api.core.config.configuration import Configuration
from food_review_api.products.repository import ProductRepository, product_repository

logger = getLogger(__name__)
router = APIRouter()


@router.get("", response_model=ProductsListResponse)
async def get_products(
    product_repository: Annotated[ProductRepository, Depends(get_product_repository)],
):
    """Get a list of all products available in the service.

    This endpoint returns a list of all products that are currently loaded in the service.

    Returns:
        ProductsListResponse: A response containing a list of all products available in
        the service.
    """
    return ProductsListResponse(
        available_products=product_repository.available_products
    )


@router.get("/most_reviewed", response_model=list[ProductReviewsCountResponse])
async def get_most_reviewed_products(
    n: Annotated[int, Query(gt=0)],
    product_repository: Annotated[ProductRepository, Depends(get_product_repository)],
):
    """Get the most reviewed products.

    This endpoint returns the top `n` products with the most reviews.

    Args:
        n (int): The number of products to return.

    Returns:
        list[ProductReviewsCountResponse]: A list of `ProductReviewsCountResponse`
        objects, each containing the `product_id` and `number_of_reviews` for the
        top `n` products.
    """
    top_reviewed_products = await product_repository.most_commented_products(n=n)
    return [
        ProductReviewsCountResponse(
            product_id=product_id, number_of_reviews=number_of_reviews
        )
        for product_id, number_of_reviews in top_reviewed_products.items()
    ]


@router.get("/least_reviewed", response_model=list[ProductReviewsCountResponse])
async def get_least_reviewed_products(
    n: Annotated[int, Query(gt=0)],
    product_repository: Annotated[ProductRepository, Depends(get_product_repository)],
):
    """Get the least reviewed products.

    This endpoint returns the bottom `n` products with the least reviews.

    Args:
        n (int): The number of products to return.

    Returns:
        list[ProductReviewsCountResponse]: A list of `ProductReviewsCountResponse`
        objects, each containing the `product_id` and `number_of_reviews` for the
        bottom `n` products.
    """
    least_reviewed_products = await product_repository.least_commented_products(n=n)
    return [
        ProductReviewsCountResponse(
            product_id=product_id, number_of_reviews=number_of_reviews
        )
        for product_id, number_of_reviews in least_reviewed_products.items()
    ]


@router.get(path="/reload", response_model=ProductsMetadataResponse)
def reload_products_from_registry(
    background_tasks: BackgroundTasks,
    config: Annotated[Configuration, Depends(fetch_configuration)],
):
    """Trigger reloading of products from product registry.

    This endpoint triggers a background task to reload products from the product registry.

    Returns a JSON response with the current products metadata.
    """
    logger.info("Triggering product reloading from product registry.")
    background_tasks.add_task(
        product_repository.load,
        db=config.database,
    )
    return ProductsMetadataResponse(products=config.database)
