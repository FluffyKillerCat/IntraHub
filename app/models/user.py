from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from datetime import datetime
from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)  # Hashed password
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=True)  # Allow NULL to prevent circular dependency

    created_at = Column(DateTime, default=datetime.utcnow)
