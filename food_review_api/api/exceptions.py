"""Food Review API error handlers definitions."""

from logging import getLogger

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from food_review_api.api.schemas.errors import HTTPErrorResponse
from food_review_api.products import ProductNotFoundInRepositoryError

logger = getLogger(__name__)


def add_exception_handlers(app: FastAPI) -> None:
    """Add error handlers to FastAPI application.

    Args:
        app: The FastAPI application instance.

    Returns:
        None
    """
    app.add_exception_handler(
        ProductNotFoundInRepositoryError, product_not_found_exception_handler
    )


def product_not_found_exception_handler(
    request: Request, exc: ProductNotFoundInRepositoryError
) -> JSONResponse:
    """Error handler for ProductNotFoundInRepositoryError exception.

    Args:
        request: The incoming request.
        exc: The exception instance.

    Returns:
        JSONResponse: The response to the client.
    """
    model_key = exc.args[0]
    msg = f"Product with key '{model_key}' not loaded in the service."
    logger.exception(msg)
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=HTTPErrorResponse(detail=msg).model_dump(),
    )
