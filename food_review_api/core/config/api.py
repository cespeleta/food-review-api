"""Food Review API configuration class definition."""

from pydantic import AnyHttpUrl, BaseModel, Field
from pydantic_core import Url


class ApiConfig(BaseModel):
    """Api configuration model."""

    title: str = "Food Review API"
    description: str = "Food Review REST API to provide reviews from Amazon products."
    openapi_url: str = "/common/api-docs"
    base_url: AnyHttpUrl = Field(
        default=Url("http://localhost:8000"),
        title="Base URL to call service.",
    )
