from pydantic import BaseModel
from datetime import datetime

class UserOrgCreate(BaseModel):
    user: int
    org: int
    accepted_by: int

class UserOrgOut(BaseModel):

    org: int
    accepted_by: int
    joined_on: datetime
    class Config:
        orm_mode: True


