# schemas/steps.py
from pydantic import BaseModel, Field

class RecipeStepCreate(BaseModel):
    step_number: int = Field(..., example=1)
    instruction: str = Field(..., example="Preheat oven to 350°F.")
