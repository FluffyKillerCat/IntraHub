from pydantic import BaseModel, model_validator
from datetime import datetime

class EventCreate(BaseModel):
    title: str
    description: str
    location: str
    event_type: str
    event_date: datetime
    start_time: datetime
    end_time: datetime
    max_attendees: int
    invitation_type: str  # 'invited' or 'ticket_request'

    @model_validator(mode="after")
    def validate_event_mode(cls, values):

        event_date  = datetime.strptime(values["event_date"], "%Y-%m-%d")
        if event_date < datetime.now():
            raise ValueError("Event date must be before today")
        event_start_time = datetime.strptime(values["start_time"], "%H:%M:%S")
        event_end_time = datetime.strptime(values["end_time"], "%H:%M:%S")

        if event_start_time > event_end_time:
            raise ValueError("Event start time must be before event end time")
        return values



class EventOut(BaseModel):
    id: int
    creator_id: int
    title: str
    description: str
    location: str
    event_type: str
    start_time: datetime
    end_time: datetime
    max_attendees: int
    invitation_type: str
    created_at: datetime

    class Config:
        orm_mode = True
