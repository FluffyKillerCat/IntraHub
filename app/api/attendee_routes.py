from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.attendee_schema import AttendeeCreate, AttendeeOut
from app.models.event_attendee import EventAttendee
from app.db.session import SessionLocal
from app.api.user_routes import get_current_user
from app.models.event import Event
from app.dependencies.oauth2_scheme import oauth2_scheme
from app.utilities.jwt import decode_access_token
router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=AttendeeOut)
def register_attendee(attendee_in: AttendeeCreate, current_user = Depends(get_current_user), db: Session = Depends(get_db), token = Depends(oauth2_scheme)):
    payload = decode_access_token(token)

    event_count = db.query(Event.max_attendees).filter(Event.id == attendee_in.event_id).scalar()

    if not event_count:
        raise HTTPException(status_code=404, detail="Event not found")
    attendee = EventAttendee(
        event_id=attendee_in.event_id,
        user_id=current_user.id,
        registration_mode="invited",
        status="accepted"
    )
    if db.query(EventAttendee).filter_by(event_id=attendee.event_id).count() < event_count:
        db.add(attendee)
        db.commit()
        db.refresh(attendee)
        return attendee
    else:
        raise HTTPException(status_code=401, detail="Event Full!!!")

