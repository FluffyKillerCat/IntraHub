from sqlalchemy import ForeignKey, Column, Integer, DateTime, Boolean, String
from datetime import datetime
from app.db.base import Base


class UserOrgs(Base):
    __tablename__ = "user_orgs"


    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey('users.username'), nullable=True)
    part_of = Column(String, ForeignKey('organizations.org_name'), nullable=True)
    is_admin = Column(Boolean, default=False)
    date_joined = Column(DateTime, default=datetime.utcnow)
