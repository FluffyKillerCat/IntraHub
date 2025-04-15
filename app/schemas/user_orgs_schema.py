from pydantic import BaseModel
from datetime import datetime

class UserOrgCreate(BaseModel):
    username: str
    part_of: str


class UserOrgOut(BaseModel):

    user_id: int
    part_of: str
    class Config:
        orm_mode: True


