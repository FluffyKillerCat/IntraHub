from sqlalchemy import Column, ForeignKey, Integer, String
from app.db.base import Base


class organizations(Base):

    __tablename__ = "organizations"
    id = Column(Integer, primary_key=True, autoincrement=True)
    admin_id = Column(Integer, ForeignKey("users.id"))
    org_name = Column(String(50), nullable=False, comment="e.g., organization name")


