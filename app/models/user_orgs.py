from sqlalchemy import ForeignKey, Column, Integer, DateTime, Boolean
from datetime import datetime
from app.db.base import Base


class UserOrgs(Base):
    __tablename__ = "user_orgs"


    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    part_of = Column(Integer, ForeignKey('organizations.id'), nullable=True)
    is_admin = Column(Boolean, default=False)
    date_joined = Column(DateTime, default=datetime.utcnow)

