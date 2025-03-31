from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from app.db.base import Base


class EventAttendee(Base):
    __tablename__ = "event_attendees"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    registration_mode = Column(String(50), nullable=False, comment="Either 'invited' or 'requested'")
    status = Column(String(50), nullable=False, comment="e.g., pending, approved, attended, declined")
    registered_at = Column(DateTime, default=datetime.utcnow)
