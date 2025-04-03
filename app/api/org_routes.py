from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.organization_schema import OrganizationCreate, OrganizationOut
from app.models.organizations import Organizations
from app.db.session import SessionLocal
from app.api.user_routes import get_current_user
from app.services.org_service import create_org, add_user_to_org
from app.schemas.user_orgs_schema import UserOrgCreate, UserOrgOut


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.post("/", response_model=OrganizationOut)
def make_new_org(org_in: OrganizationCreate, db: Session = Depends(get_db), curr_user = Depends(get_current_user)):
    org = create_org(db, org_in, admin=curr_user)
    return org

@router.post("/add_user", response_model=UserOrgOut)
def add_user_to_org(user_in: UserOrgCreate, db: Session = Depends(get_db), curr_user = Depends(get_current_user)):
    new_user = add_user_to_org(db, user_in, curr_user)
    return new_user
