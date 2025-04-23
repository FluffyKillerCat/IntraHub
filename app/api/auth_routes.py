from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.user_schema import UserCreate, UserOut, Token, RToken
from app.services import auth_service
from app.db.session import SessionLocal
from app.dependencies.oauth2_scheme import oauth2_scheme
from app.utilities.jwt import decode_refresh_token
from app.services.auth_service import get_user_by_username
from fastapi import APIRouter, HTTPException, Header, Depends, status, Request
from sqlalchemy.orm import Session
router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=UserOut)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    if auth_service.get_user_by_username(db, user_data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    new_user = auth_service.create_user(db, user_data.username, user_data.email, user_data.password)
    return new_user

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth_service.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token = auth_service.generate_token_for_user(user, db)
    refresh_token = auth_service.generate_rtoken_for_user(user, db)



    return {"access_token": access_token,  "token_type": "bearer"}


@router.post("/token/refresh", response_model=Token)
def refresh_access_token(
    refresh_token: str = Depends(oauth2_scheme),  # Extract refresh token via Authorization header
    db: Session = Depends(get_db)
):
    try:

        # Decode and validate the refresh token
        payload = decode_refresh_token(refresh_token)

        user = get_user_by_username(db, payload["sub"])
        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found."
            )

        # Generate new tokens
        new_access_token = auth_service.generate_token_for_user(user, db)
        new_refresh_token = auth_service.generate_rtoken_for_user(user, db)

        return {
            "access_token": new_access_token,

            "token_type": "bearer"
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token refresh failed: {e}"
        )



