from pydantic import BaseModel, model_validator
from datetime import datetime, time, date


class EventCreate(BaseModel):
    title: str
    description: str
    location: str
    event_type: str
    event_date: date
    start_time: time
    end_time: time
    max_attendees: int
    invitation_type: str  # 'invited' or 'ticket_request'

    @model_validator(mode="after")
    def validate_event_mode(cls, model):
        # Validate event date
        if model.event_date < date.today():
            raise ValueError("Event date must be in the future.")

        # Validate start and end times
        if model.start_time >= model.end_time:
            raise ValueError("Event start time must be before event end time.")

        return model



class EventOut(BaseModel):
    id: int
    creator_id: int
    title: str
    description: str
    location: str
    event_type: str
    event_date: date
    start_time: time
    end_time: time
    max_attendees: int
    invitation_type: str
    created_at: datetime

    class Config:
        orm_mode = True
