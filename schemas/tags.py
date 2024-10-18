from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

# Schema for creating a new tag
class TagCreate(BaseModel):
    name: str = Field(..., example="Quick Meal")

# Schema for updating an existing tag
class TagUpdate(BaseModel):
    name: Optional[str] = Field(None, example="Healthy Eating")

# Schema for responses with the ID included
class TagResponse(BaseModel):
    id: int
    name: str

    # Use the new `from_attributes` config to allow SQLAlchemy models as input
    model_config = ConfigDict(from_attributes=True)
