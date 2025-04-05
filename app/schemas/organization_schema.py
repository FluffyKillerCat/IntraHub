from pydantic import BaseModel
from datetime import datetime


class OrganizationCreate(BaseModel):
    name: str


class OrganizationOut(BaseModel):
    org_name: str
    created_id: str

    class Config:
        orm_mode = True