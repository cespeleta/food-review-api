from pydantic import BaseModel, Field


class Review(BaseModel):
    """Review class."""

    id: int
    product_id: str = Field(description="Unique identifier for the product")
    user_id: str = Field(description="Unqiue identifier for the user")
    profile_name: str = Field(description="Profile name of the user")
    helpfulness_numerator: int = Field(
        description="Number of users who found the review helpful"
    )
    helpfulness_denominator: int = Field(
        description="Number of users who indicated whether they found the review helpful or not"
    )
    score: int = Field(ge=0, le=5, description="Rating between 1 and 5")
    time: int = Field(description="Timestamp for the review")
    summary: str = Field(description="Brief summary of the review")
    text: str = Field(description="Text of the review")
