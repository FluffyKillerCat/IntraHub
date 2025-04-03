from pydantic import BaseModel
from datetime import datetime


class OrganizationCreate(BaseModel):
    id: int
    name: str
    administrator_id: int

class OrganizationOut(BaseModel):
    name: str
    created_by: str

    class Config:
        orm_mode = True