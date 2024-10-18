# routers/ingredients.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    item = Column(String(100), index=True)
    quantity = Column(String(50))
    notes = Column(String(255))
    price = Column(Integer)
    currency = Column(String(3))

    # Many-to-Many relationship with Recipe
    recipes = relationship(
        "Recipe", secondary="recipe_ingredients", back_populates="ingredients"
    )
