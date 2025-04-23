from sqlalchemy import Column, Integer, String, Text, ForeignKey
from app.db.base import Base


class Speaker(Base):
    __tablename__ = "speakers"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.title"), nullable=False)
    name = Column(String(100), nullable=False)
    bio = Column(Text, nullable=False)
