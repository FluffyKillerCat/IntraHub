
from pydantic import BaseModel
from datetime import datetime

class InvitationCreate(BaseModel):
    event_id: str
    invitee_email: str

class InvitationOut(BaseModel):
    id: int
    event_id: int
    inviter_id: int
    invitee_email: str
    token: str
    status: str
    sent_at: datetime

    class Config:
        orm_mode = True
