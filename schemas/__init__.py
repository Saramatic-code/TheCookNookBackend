# schemas/recipes.py
from pydantic import BaseModel
from typing import List

# Import other schemas after Pydantic and typing
from schemas.ingredients import IngredientCreate
from schemas.categories import CategoryCreate
from schemas.tags import TagCreate
from schemas.nutrition import NutritionFactsCreate  # This should come after others
from schemas.steps import RecipeStepCreate
