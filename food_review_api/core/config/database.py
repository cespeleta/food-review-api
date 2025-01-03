"""Food Review API database configuration class definition."""

from pydantic import BaseModel, Field, field_validator


class DatabaseConfig(BaseModel):
    """Database configuration model."""

    filename: str = Field(frozen=True)
    version: str = "1"

    @field_validator("version", mode="before")
    def cast_version_to_string(cls, value: int | str):
        """Validator to cast version integers to strings."""
        return str(value) if isinstance(value, int) else value
