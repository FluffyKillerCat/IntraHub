from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from app.schemas.user_schema import UserOut
from app.services.auth_service import get_user_by_username
from app.utilities.jwt import decode_access_token
from app.db.session import SessionLocal
from app.db.database import get_db

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# Dependency to get database session


# Dependency to get the current user
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):

    try:
        # Decode the JWT token
        payload = decode_access_token(token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    if not payload or "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials!!!"
        )

    # Fetch user from database using their username (from payload)

    user = get_user_by_username(db, payload["sub"])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    # Return the user object
    return user


# /me route
@router.get("/me", response_model=UserOut)
def read_users_me(current_user: UserOut = Depends(get_current_user)):
    return current_user

@router.get("/secure")
def secure_endpoint(token: str = Depends(oauth2_scheme)):

    return {"token": token}

@router.delete("/users/{username}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_by_username(
    username: str,
    current_user: UserOut = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Optional: Prevent users from deleting others unless admin
    if username != current_user.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this user"
        )

    user = get_user_by_username(db, username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    db.delete(user)
    db.commit()

    return {"detail": f"User '{username}' deleted successfully"}
