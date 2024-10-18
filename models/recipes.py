# models/recipes.py

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base

# Association table between recipes and ingredients
recipe_ingredients = Table(
    'recipe_ingredients', Base.metadata,
    Column('recipe_id', Integer, ForeignKey('recipes.id'), primary_key=True),
    Column('ingredient_id', Integer, ForeignKey('ingredients.id'), primary_key=True)
)

# Association table between recipes and categories
recipe_categories = Table(
    'recipe_categories', Base.metadata,
    Column('recipe_id', Integer, ForeignKey('recipes.id'), primary_key=True),
    Column('category_id', Integer, ForeignKey('categories.id'), primary_key=True)
)

# Association table between recipes and tags
recipe_tags = Table(
    'recipe_tags', Base.metadata,
    Column('recipe_id', Integer, ForeignKey('recipes.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)

class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, index=True, nullable=False)
    prep_time_value = Column(Integer)
    prep_time_unit = Column(String(10))
    cook_time_value = Column(Integer)
    cook_time_unit = Column(String(10))
    servings = Column(Integer)
    image = Column(String, nullable=True)
    deleted = Column(Boolean, default=False)

    # One-to-Many relationship: Instructions
    instructions = relationship(
        "RecipeStep", back_populates="recipe", cascade="all, delete-orphan"
    )

    # One-to-One relationship: Nutrition Facts
    nutrition_facts = relationship(
        "NutritionFacts", back_populates="recipe", uselist=False, cascade="all, delete-orphan"
    )

    # Many-to-Many relationships: Ingredients, Categories, Tags
    ingredients = relationship(
        "Ingredient", secondary=recipe_ingredients, back_populates="recipes"
    )
    categories = relationship(
        "Category", secondary=recipe_categories, back_populates="recipes"
    )
    tags = relationship(
        "Tag", secondary=recipe_tags, back_populates="recipes"
    )
