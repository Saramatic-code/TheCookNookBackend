# main.py
from fastapi import FastAPI, HTTPException
from sqlalchemy import Column, Integer, String, ForeignKey, Table, Boolean
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from typing import List, Optional
# schemas/recipes.py
from pydantic import BaseModel
from schemas.ingredients import IngredientCreate
from schemas.recipes import RecipeCreate
from schemas.tags import TagCreate
from schemas.nutrition import NutritionFactsCreate  
from schemas.steps import RecipeStepCreate 
from routers import recipes, tags



# Import database components
from database import Base, engine, SessionLocal  

# FastAPI setup
app = FastAPI()

# CORS middleware to allow cross-origin resource sharing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins, or restrict it to your frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create all tables
Base.metadata.create_all(bind=engine)

# Dependency to get the session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ------------------------ Routes ------------------------
# Register the API router
# app.include_router(api_router)
app.include_router(recipes.router, prefix="/recipes", tags=["recipes"])

# Register the tags router
app.include_router(tags.router, prefix="/tags", tags=["tags"])



