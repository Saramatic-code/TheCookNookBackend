# schemas/categories.py
from pydantic import BaseModel, Field

class CategoryCreate(BaseModel):
    name: str = Field(..., example="Vegetarian")
