from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.organization_schema import OrganizationCreate, OrganizationOut
from app.models.organizations import Organizations
from app.db.session import SessionLocal
from app.api.user_routes import get_current_user
from app.services.org_service import create_org, add_user_to
from app.schemas.user_orgs_schema import UserOrgCreate, UserOrgOut
from app.dependencies.oauth2_scheme import oauth2_scheme

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.post("/", response_model=OrganizationOut)
def make_new_org(org_in: OrganizationCreate, db: Session = Depends(get_db), curr_user = Depends(get_current_user), token:str = Depends(oauth2_scheme)):


    org = create_org(token=token, db=db, org_in=org_in, admin=curr_user)
    return org

@router.post("/add_user", response_model=UserOrgOut)
def add_user_to_org(user_in: UserOrgCreate, db: Session = Depends(get_db), curr_user = Depends(get_current_user), token = Depends(oauth2_scheme)):
    try:
        new_user = add_user_to(token=token, db=db, user_org_data=user_in, admin=curr_user)
        if not new_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User Not Auth to add to org"
            )
        return new_user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"{e}"
        )
