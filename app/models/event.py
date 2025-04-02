from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Time, Date, ARRAY
from datetime import datetime
from app.db.base import Base


class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(150), nullable=False)
    description = Column(Text, nullable=False)
    location = Column(String(255), nullable=False)
    event_type = Column(String(50), nullable=False)
    event_date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    max_attendees = Column(Integer, nullable=False)
    invitation_type = Column(String(50), nullable=False, comment="e.g., 'invited' or 'ticket_request'")
    created_at = Column(DateTime, default=datetime.utcnow)
