from pydantic import BaseModel
from datetime import datetime

class AttendeeCreate(BaseModel):
    event_id: int
    registration_mode: str  # "invited" or "requested"

class AttendeeOut(BaseModel):
    id: int
    event_id: int
    user_id: int
    registration_mode: str
    status: str
    registered_at: datetime

    class Config:
        orm_mode = True
