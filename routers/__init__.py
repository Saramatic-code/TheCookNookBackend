# routers/__init__.py
# from fastapi import APIRouter
# from routers.recipes import router as recipes_router

# router = APIRouter()
# router.include_router(recipes_router, prefix="/recipes", tags=["Recipes"])

# routers/__init__.py
from .recipes import router as recipes_router
from .tags import router as tags_router
