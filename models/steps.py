# routers/steps.py
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import Base

class RecipeStep(Base):
    __tablename__ = "instructions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)
    step_number = Column(Integer, nullable=False)
    instruction = Column(String, nullable=False)
    deleted = Column(Boolean, default=False)

    # Relationship with Recipe
    recipe = relationship("Recipe", back_populates="instructions")
