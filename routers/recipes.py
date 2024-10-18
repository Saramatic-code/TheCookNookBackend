# routers/recipes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

# Import necessary models and schemas
from models import Recipe, Ingredient, Category, Tag, RecipeStep, NutritionFacts
from database import get_db
from schemas.recipes import RecipeCreate, RecipeUpdate


router = APIRouter()

# ------------------------ GET Routes ------------------------

# routers/recipes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from models import Recipe, Ingredient, Category, Tag, RecipeStep, NutritionFacts
from schemas.recipes import RecipeCreate, RecipeUpdate
from database import get_db

router = APIRouter()

# ------------------------ GET Routes ------------------------

@router.get("/")
def get_recipes(db: Session = Depends(get_db)):
    """
    Retrieve all recipes, including their details.
    """
    recipes = db.query(Recipe).filter(Recipe.deleted.is_(False)).all()
    return {
        "recipes": [
            {
                "id": recipe.id,
                "title": recipe.title,
                "prep_time_value": recipe.prep_time_value,
                "prep_time_unit": recipe.prep_time_unit,
                "cook_time_value": recipe.cook_time_value,
                "cook_time_unit": recipe.cook_time_unit,
                "servings": recipe.servings,
                "image": recipe.image,
                "instructions": [
                    {"step_number": step.step_number, "instruction": step.instruction}
                    for step in recipe.instructions if not step.deleted
                ],
                "nutrition_facts": {
                    "calories": recipe.nutrition_facts.calories,
                    "fat": recipe.nutrition_facts.fat,
                    "carbohydrates": recipe.nutrition_facts.carbohydrates,
                    "protein": recipe.nutrition_facts.protein,
                } if recipe.nutrition_facts else None,
                "ingredients": [
                    {
                        "item": ingredient.item,
                        "quantity": ingredient.quantity,
                        "notes": ingredient.notes,
                        "price": ingredient.price,
                        "currency": ingredient.currency,
                    }
                    for ingredient in recipe.ingredients
                ],
                "categories": [category.name for category in recipe.categories],
                "tags": [tag.name for tag in recipe.tags],
            }
            for recipe in recipes
        ]
    }

@router.get("/{id}")
def get_recipe_by_id(id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single recipe by its ID.
    """
    recipe = db.query(Recipe).filter(Recipe.id == id, Recipe.deleted.is_(False)).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    return {
        "id": recipe.id,
        "title": recipe.title,
        "prep_time_value": recipe.prep_time_value,
        "prep_time_unit": recipe.prep_time_unit,
        "cook_time_value": recipe.cook_time_value,
        "cook_time_unit": recipe.cook_time_unit,
        "servings": recipe.servings,
        "image": recipe.image,
        "instructions": [
            {"step_number": step.step_number, "instruction": step.instruction}
            for step in recipe.instructions if not step.deleted
        ],
        "nutrition_facts": {
            "calories": recipe.nutrition_facts.calories,
            "fat": recipe.nutrition_facts.fat,
            "carbohydrates": recipe.nutrition_facts.carbohydrates,
            "protein": recipe.nutrition_facts.protein,
        } if recipe.nutrition_facts else None,
        "ingredients": [
            {
                "item": ingredient.item,
                "quantity": ingredient.quantity,
                "notes": ingredient.notes,
                "price": ingredient.price,
                "currency": ingredient.currency,
            }
            for ingredient in recipe.ingredients
        ],
        "categories": [category.name for category in recipe.categories],
        "tags": [tag.name for tag in recipe.tags],
    }


# ------------------------ POST Route ------------------------

@router.post("/")
def create_recipe(recipe: RecipeCreate, db: Session = Depends(get_db)):
    # Normalize and capitalize the title
    normalized_title = recipe.title.strip().capitalize()

    # Check if the recipe already exists (case-insensitive)
    existing_recipe = db.query(Recipe).filter(Recipe.title.ilike(normalized_title)).first()
    if existing_recipe:
        raise HTTPException(status_code=400, detail="Recipe already exists")

    # Create a new recipe instance with the normalized title
    new_recipe = Recipe(
        title=normalized_title,
        prep_time_value=recipe.prep_time_value,
        prep_time_unit=recipe.prep_time_unit,
        cook_time_value=recipe.cook_time_value,
        cook_time_unit=recipe.cook_time_unit,
        servings=recipe.servings,
        image=recipe.image,
    )

    # Add nutrition facts
    new_nutrition_facts = NutritionFacts(
        calories=recipe.nutrition_facts.calories,
        fat=recipe.nutrition_facts.fat,
        carbohydrates=recipe.nutrition_facts.carbohydrates,
        protein=recipe.nutrition_facts.protein,
        recipe=new_recipe
    )
    new_recipe.nutrition_facts = new_nutrition_facts

    # Normalize and add instructions
    for step in recipe.instructions:
        new_step = RecipeStep(
            step_number=step.step_number,
            instruction=step.instruction.strip().capitalize(),  # Capitalize each instruction
            recipe=new_recipe
        )
        new_recipe.instructions.append(new_step)

    # Normalize and add ingredients with checks
    for ingredient_data in recipe.ingredients:
        normalized_item = ingredient_data.item.strip().capitalize()
        existing_ingredient = db.query(Ingredient).filter(
            Ingredient.item.ilike(normalized_item)
        ).first()
        if existing_ingredient:
            new_recipe.ingredients.append(existing_ingredient)
        else:
            new_ingredient = Ingredient(
                item=normalized_item,
                quantity=ingredient_data.quantity,
                notes=ingredient_data.notes,
                price=ingredient_data.price,
                currency=ingredient_data.currency
            )
            db.add(new_ingredient)
            new_recipe.ingredients.append(new_ingredient)

    # Normalize and add categories with checks
    for category_data in recipe.categories:
        normalized_category = category_data.name.strip().capitalize()
        existing_category = db.query(Category).filter(
            Category.name.ilike(normalized_category)
        ).first()
        if existing_category:
            new_recipe.categories.append(existing_category)
        else:
            new_category = Category(name=normalized_category)
            db.add(new_category)
            new_recipe.categories.append(new_category)

    # Normalize and add tags with checks
    for tag_data in recipe.tags:
        normalized_tag = tag_data.name.strip().capitalize()
        existing_tag = db.query(Tag).filter(Tag.name.ilike(normalized_tag)).first()
        if existing_tag:
            new_recipe.tags.append(existing_tag)
        else:
            new_tag = Tag(name=normalized_tag)
            db.add(new_tag)
            new_recipe.tags.append(new_tag)

    # Commit the recipe and associated data
    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)

    return {"message": f"Recipe added: {new_recipe.title}"}


# ------------------------ PUT Route ------------------------

@router.post("/")
def create_recipe(recipe: RecipeCreate, db: Session = Depends(get_db)):
    # Check if the recipe already exists
    existing_recipe = db.query(Recipe).filter(Recipe.title.ilike(recipe.title)).first()
    if existing_recipe:
        raise HTTPException(status_code=400, detail="Recipe already exists")

    # Create a new recipe instance
    new_recipe = Recipe(
        title=recipe.title,
        prep_time_value=recipe.prep_time_value,
        prep_time_unit=recipe.prep_time_unit,
        cook_time_value=recipe.cook_time_value,
        cook_time_unit=recipe.cook_time_unit,
        servings=recipe.servings,
        image=recipe.image,
    )

    # Add nutrition facts
    new_nutrition_facts = NutritionFacts(
        calories=recipe.nutrition_facts.calories,
        fat=recipe.nutrition_facts.fat,
        carbohydrates=recipe.nutrition_facts.carbohydrates,
        protein=recipe.nutrition_facts.protein,
        recipe=new_recipe
    )
    new_recipe.nutrition_facts = new_nutrition_facts

    # Add instructions
    for step in recipe.instructions:
        new_step = RecipeStep(
            step_number=step.step_number, 
            instruction=step.instruction, 
            recipe=new_recipe
        )
        new_recipe.instructions.append(new_step)

    # Add ingredients with checks
    for ingredient_data in recipe.ingredients:
        existing_ingredient = db.query(Ingredient).filter(
            Ingredient.item == ingredient_data.item
        ).first()
        if existing_ingredient:
            new_recipe.ingredients.append(existing_ingredient)
        else:
            new_ingredient = Ingredient(
                item=ingredient_data.item,
                quantity=ingredient_data.quantity,
                notes=ingredient_data.notes,
                price=ingredient_data.price,
                currency=ingredient_data.currency
            )
            db.add(new_ingredient)
            new_recipe.ingredients.append(new_ingredient)

    # Add categories with checks
    for category_data in recipe.categories:
        existing_category = db.query(Category).filter(
            Category.name == category_data.name
        ).first()
        if existing_category:
            new_recipe.categories.append(existing_category)
        else:
            new_category = Category(name=category_data.name)
            db.add(new_category)
            new_recipe.categories.append(new_category)

    # Add tags with checks
    for tag_data in recipe.tags:
        existing_tag = db.query(Tag).filter(
            Tag.name == tag_data.name
        ).first()
        if existing_tag:
            new_recipe.tags.append(existing_tag)
        else:
            new_tag = Tag(name=tag_data.name)
            db.add(new_tag)
            new_recipe.tags.append(new_tag)

    # Add the new recipe to the session and commit
    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)

    return {"message": f"Recipe added: {new_recipe.title}"}
