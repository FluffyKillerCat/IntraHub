from pydantic import BaseModel
from datetime import datetime

class UserOrgCreate(BaseModel):
    user_id: int
    part_of: int


class UserOrgOut(BaseModel):

    user_id: int
    part_of: int
    class Config:
        orm_mode: True


