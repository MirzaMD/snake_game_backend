from pydantic import BaseModel, Field

class SnakeBoard(BaseModel):
    user: str = Field(default="Guest", description="Username's field")
    score: int = Field(...)