from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

# Import necessary models and schemas
from models import Tag
from schemas.tags import TagCreate, TagUpdate, TagResponse
from database import get_db

# Define the APIRouter instance
router = APIRouter()

# ------------------------ GET All Tags ------------------------

@router.get("/", response_model=List[TagResponse])
def get_all_tags(db: Session = Depends(get_db)):
    """
    Retrieve all tags.
    """
    tags = db.query(Tag).all()
    return tags

# ------------------------ GET Tag by ID ------------------------

@router.get("/{tag_id}", response_model=TagResponse)
def get_tag_by_id(tag_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific tag by ID.
    """
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag

# ------------------------ POST Route ------------------------

@router.post("/", response_model=TagResponse, status_code=201)
def create_tag(tag: TagCreate, db: Session = Depends(get_db)):
    """
    Create a new tag or return the existing one.
    """
    # Normalize tag name to capitalize the first letter
    normalized_name = tag.name.strip().capitalize()

    # Check if the tag already exists (case-insensitive search)
    existing_tag = db.query(Tag).filter(Tag.name.ilike(normalized_name)).first()
    if existing_tag:
        return existing_tag

    # Create and add new tag if it doesn't exist
    new_tag = Tag(name=normalized_name)
    db.add(new_tag)
    db.commit()
    db.refresh(new_tag)

    return new_tag

# ------------------------ PUT Route ------------------------

@router.put("/{tag_id}", response_model=TagResponse)
def update_tag(tag_id: int, tag_update: TagUpdate, db: Session = Depends(get_db)):
    """
    Update an existing tag by ID, or prevent duplicate tags.
    """
    existing_tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not existing_tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    if tag_update.name:
        normalized_name = tag_update.name.strip().capitalize()

        # Check if another tag with the same name exists (case-insensitive)
        duplicate_tag = db.query(Tag).filter(
            Tag.name.ilike(normalized_name), Tag.id != tag_id
        ).first()
        if duplicate_tag:
            raise HTTPException(
                status_code=400, detail=f"Tag '{normalized_name}' already exists"
            )

        existing_tag.name = normalized_name

    db.commit()
    db.refresh(existing_tag)
    return existing_tag

# ------------------------ DELETE Route ------------------------

@router.delete("/{tag_id}", status_code=204)
def delete_tag(tag_id: int, db: Session = Depends(get_db)):
    """
    Delete a tag by ID.
    """
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    db.delete(tag)
    db.commit()
    return {"message": f"Tag with ID {tag_id} has been deleted"}
