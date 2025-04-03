from pydantic import BaseModel
from datetime import datetime


class OrganizationCreate(BaseModel):
    name: str


class OrganizationOut(BaseModel):
    name: str
    created_by: str

    class Config:
        orm_mode = True