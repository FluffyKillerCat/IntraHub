from sqlalchemy import Column, Integer, ForeignKey
from app.db.base import Base


class EventCategory(Base):
    __tablename__ = "event_categories"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
