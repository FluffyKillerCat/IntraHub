from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.speaker_schema import SpeakerCreate, SpeakerOut
from app.models.speaker import Speaker
from app.db.session import SessionLocal
from app.api.user_routes import get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=SpeakerOut)
def add_speaker(speaker_in: SpeakerCreate, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    speaker = Speaker(
        event_id=speaker_in.event_id,
        name=speaker_in.name,
        bio=speaker_in.bio

    )
    db.add(speaker)
    db.commit()
    db.refresh(speaker)
    return speaker
