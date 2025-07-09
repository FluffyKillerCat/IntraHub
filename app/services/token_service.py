from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

from app.utilities.jwt import decode_access_token
from app.db.session import SessionLocal
from sqlalchemy.orm import Session
from app.services.auth_service import get_user_by_username



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_token(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    token = oauth2_scheme()


    try:
        # Decode the JWT token


        payload = decode_access_token(token)




    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"{e}"
        )
    if not payload:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail= "no payload"
        )


    if "sub" not in payload: #if not payload or "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"{payload}"
        )

    # Fetch user from database using their username (from payload)
    user = get_user_by_username(db, payload["sub"])


    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid User"
        )

    # Return the user object
    return payload
