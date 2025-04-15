from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.event_schema import EventCreate, EventOut
from app.schemas.user_schema import UserOut
from app.services.event_service import create_event, get_all_events, get_event_by_id
from app.db.session import SessionLocal
from app.api.user_routes import get_current_user
from app.dependencies.oauth2_scheme import oauth2_scheme
router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=EventOut)
def create_new_event(event_in: EventCreate, current_user = Depends(get_current_user), db: Session = Depends(get_db), token = Depends(oauth2_scheme)):
    try:
        event = create_event(db, current_user, event_in, token)
        return event
    except ValueError as e:
        raise HTTPException(status_code=404, detail=f"{e}")

@router.get("/", response_model=list[EventOut])
def list_events(db: Session = Depends(get_db), current_user: UserOut = Depends(get_current_user), token = Depends(oauth2_scheme)):
    events = get_all_events(db, current_user.id, token)
    return events


@router.get("/{event_id}", response_model=EventOut)
def get_event(event_id: int, db: Session = Depends(get_db), current_user: UserOut = Depends(get_current_user)):
    event = get_event_by_id(db, event_id, current_user.id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    else:
        return event
