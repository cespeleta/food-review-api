"""Food Review API health router definition."""

from fastapi import APIRouter, status
from pydantic import BaseModel

router = APIRouter(tags=["Health"])


class HealthCheck(BaseModel):
    """Response model to validate and return when performing a health check."""

    status: str = "OK"


@router.get(
    "/health",
    summary="Perform a Health Check",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
    response_model=HealthCheck,
)
def get_health() -> HealthCheck:
    """Perform a Health Check.

    This endpoint can primarily be used by Docker to ensure a robust container
    orchestration and management is in place.

    Returns:
        HealthCheck: Returns a JSON response with the health status
    """
    return HealthCheck(status="OK")
