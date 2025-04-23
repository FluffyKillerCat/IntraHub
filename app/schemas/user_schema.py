from pydantic import BaseModel, model_validator, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    @model_validator(mode="after")
    def validate_email(cls, values):
        username = values.username.lower()
        email = values.email.lower()
        password = values.password.lower()

        if len(password) <= 8:
            raise ValueError("Please use a password longer than 8")
        elif username in password or email in password:
            raise ValueError("Password can not contain fragments of your user name or password")
        return values



class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True




class Token(BaseModel):
    access_token: str
    token_type: str

class RToken(BaseModel):
    refresh_token: str

