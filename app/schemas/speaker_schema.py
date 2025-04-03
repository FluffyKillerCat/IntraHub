from pydantic import BaseModel

class SpeakerCreate(BaseModel):
    event_id: int
    name: str
    bio: str
    org: int

class SpeakerOut(BaseModel):
    id: int
    org: str
    event_id: int
    name: str
    bio: str

    class Config:
        orm_mode = True
