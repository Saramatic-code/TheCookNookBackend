# schemas/recipes.py
from pydantic import BaseModel
from typing import List, Optional
from schemas.ingredients import IngredientCreate
from schemas.categories import CategoryCreate
from schemas.tags import TagCreate
from schemas.nutrition import NutritionFactsCreate
from schemas.steps import RecipeStepCreate

# Schema for creating a recipe
class RecipeCreate(BaseModel):
    title: str
    prep_time_value: int
    prep_time_unit: str
    cook_time_value: int
    cook_time_unit: str
    servings: int
    image: Optional[str] = None
    nutrition_facts: NutritionFactsCreate
    instructions: List[RecipeStepCreate]
    ingredients: List[IngredientCreate]
    categories: List[CategoryCreate]
    tags: List[TagCreate]

# Schema for updating a recipe (all fields are optional for partial updates)
class RecipeUpdate(BaseModel):
    title: Optional[str] = None
    prep_time_value: Optional[int] = None
    prep_time_unit: Optional[str] = None
    cook_time_value: Optional[int] = None
    cook_time_unit: Optional[str] = None
    servings: Optional[int] = None
    image: Optional[str] = None
    nutrition_facts: Optional[NutritionFactsCreate] = None
    instructions: Optional[List[RecipeStepCreate]] = None
    ingredients: Optional[List[IngredientCreate]] = None
    categories: Optional[List[CategoryCreate]] = None
    tags: Optional[List[TagCreate]] = None
