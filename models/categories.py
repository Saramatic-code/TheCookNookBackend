# models/categories.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), unique=True, index=True)

    # Many-to-Many relationship with Recipe
    recipes = relationship(
        "Recipe", secondary="recipe_categories", back_populates="categories"
    )

