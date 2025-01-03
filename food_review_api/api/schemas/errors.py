"""Food Review API error schema definitions."""

from pydantic import BaseModel


class HTTPErrorResponse(BaseModel):
    """Error API response model."""

    detail: str
