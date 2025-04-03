from sqlalchemy import ForeignKey, Column, Integer, String, DateTime
from datetime import datetime
from app.db.base import Base


class UserOrgs(Base):
    __tablename__ = "user_orgs"

    id = Column(Integer, primary_key=True, index=True)
    part_of = Column(Integer, ForeignKey('organizations.id'))
    date_joined = Column(DateTime, default=datetime.utcnow())