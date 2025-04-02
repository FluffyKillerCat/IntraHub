from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.invitation_schema import InvitationCreate, InvitationOut
from app.models.invitation import Invitation
from app.db.session import SessionLocal
from app.api.user_routes import get_current_user
import uuid

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=InvitationOut)
def create_invitation(invite_in: InvitationCreate, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    # Generate a unique token (you may use a better token generator for production)
    token = str(uuid.uuid4())
    invitation = Invitation(
        event_id=invite_in.event_id,
        inviter_id=current_user.id,
        invitee_email=invite_in.invitee_email,
        token=token,
        status="pending"
    )
    db.add(invitation)
    db.commit()
    db.refresh(invitation)
    return invitation
