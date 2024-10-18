# schemas/nutrition.py
from pydantic import BaseModel, Field

class NutritionFactsCreate(BaseModel):
    calories: str = Field(..., example="250")
    fat: str = Field(..., example="10g")
    carbohydrates: str = Field(..., example="30g")
    protein: str = Field(..., example="5g")
