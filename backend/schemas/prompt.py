from pydantic import BaseModel, Field


class PromptRequest(BaseModel):
    prompt: str = Field(
        ...,
        min_length=5,
        max_length=500,
        description="Text description of the 3D asset"
    )