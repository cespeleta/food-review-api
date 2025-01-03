"""Food Review API v1 router definition."""

from fastapi import APIRouter

from food_review_api.api.v1.routes import products, reviews

router = APIRouter()
router.include_router(router=products.router, prefix="/products", tags=["Products"])
router.include_router(router=reviews.router, prefix="/reviews", tags=["Reviews"])
