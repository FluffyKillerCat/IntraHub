from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.category_schema import CategoryCreate, CategoryOut
from app.models.category import Category
from app.db.session import SessionLocal
from app.api.user_routes import get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=CategoryOut)
def create_category(category_in: CategoryCreate, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    category = Category(name=category_in.name)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

@router.get("/", response_model=list[CategoryOut])
def list_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).all()
    return categories
