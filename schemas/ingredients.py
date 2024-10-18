# schemas/ingredients.py
from pydantic import BaseModel

class IngredientCreate(BaseModel):
    item: str
    quantity: str
    notes: str = None
    price: float
    currency: str
