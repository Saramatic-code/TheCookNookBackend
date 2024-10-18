# routers/nutrition.py
from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class NutritionFacts(Base):
    __tablename__ = "nutrition_facts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)
    calories = Column(Integer, nullable=True)
    fat = Column(Integer, nullable=True)
    carbohydrates = Column(Integer, nullable=True)
    protein = Column(Integer, nullable=True)
    deleted = Column(Boolean, default=False)

    # One-to-One relationship with Recipe
    recipe = relationship("Recipe", back_populates="nutrition_facts")
