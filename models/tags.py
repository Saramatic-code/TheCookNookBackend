# models/tags.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), unique=True, index=True)

    # Many-to-Many relationship with Recipe
    recipes = relationship(
        "Recipe", secondary="recipe_tags", back_populates="tags"
    )

