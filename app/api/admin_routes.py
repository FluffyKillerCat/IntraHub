from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from app.schemas.admin_schema import AdminCreate, AdminOut
from app.services.admin_service import add_admin_to_org
from app.utilities.jwt import decode_access_token
from app.db.session import SessionLocal
from app.api.user_routes import get_current_user




router = APIRouter()



# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.post('/', response_model=AdminOut)
def add_new_admin(db: Session = Depends(get_db),  admin_in = AdminCreate, curr_user = Depends(get_current_user)):
    admin = add_admin_to_org(db, admin_in, curr_user)
    return admin

