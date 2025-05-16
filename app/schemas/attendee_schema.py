from pydantic import BaseModel
from datetime import datetime

class AttendeeCreate(BaseModel):
    event_title: str
    user_id: str
    registration_mode: str  # "invited" or "requested"

class AttendeeOut(BaseModel):
    id: int
    event_id: int
    user_id: int


    class Config:
        orm_mode = True
