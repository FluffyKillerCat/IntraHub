from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from app.db.base import Base


class Invitation(Base):
    __tablename__ = "invitations"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    inviter_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    invitee_email = Column(String(100), nullable=False)
    token = Column(String(255), unique=True, nullable=False)
    status = Column(String(50), nullable=False, comment="e.g., pending, accepted, declined")
    sent_at = Column(DateTime, default=datetime.utcnow)
