from pydantic import EmailStr
from sqlalchemy.orm import Session
from datetime import timedelta
from app.models.user import User
from app.models.user_orgs import UserOrgs
from app.utilities.security import verify_password, get_password_hash
from app.utilities.jwt import generate_access_token, create_refresh_token
from app.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.utilities.jwt import decode_refresh_token

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, username: str, email: EmailStr, password: str):
    hashed_password = get_password_hash(password)
    new_user = User(username=username, email=email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.password):
        return None
    return user





def generate_token_for_user(user, db):


    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    user_orgs = db.query(UserOrgs.part_of, UserOrgs.is_admin).filter(UserOrgs.user_id==user.username).all()
    orgs = {user[0]: user[1] for user in user_orgs}
    data = {"sub": user.username, "orgs": orgs}

    token = generate_access_token(
        data=data, expires_delta=access_token_expires
    )
    return token


def generate_rtoken_for_user(user, db):


    access_token_expires = timedelta(minutes=120)
    user_orgs = db.query(UserOrgs.part_of, UserOrgs.is_admin).filter(UserOrgs.user_id==user.username).all()
    orgs = {user[0]: user[1] for user in user_orgs}
    data = {"sub": user.username, "orgs": orgs}

    token = create_refresh_token(
        data=data, expires_delta=access_token_expires
    )
    return token






