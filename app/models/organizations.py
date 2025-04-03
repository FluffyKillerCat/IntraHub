from sqlalchemy import Column, ForeignKey, Integer, String
from app.db.base import Base


class Organizations(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_id = Column(Integer, ForeignKey("users.username", ondelete="SET NULL"), nullable=True)  # Allow NULL to avoid circular issues
    org_name = Column(String(50), nullable=True, comment="e.g., organization name")
