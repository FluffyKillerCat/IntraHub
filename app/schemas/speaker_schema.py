from pydantic import BaseModel

class SpeakerCreate(BaseModel):
    event_id: int
    name: str
    bio: str

class SpeakerOut(BaseModel):
    id: int
    event_id: int
    name: str
    bio: str

    class Config:
        orm_mode = True
