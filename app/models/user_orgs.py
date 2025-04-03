from sqlalchemy import ForeignKey, Column, Integer, DateTime
from datetime import datetime
from app.db.base import Base


class UserOrgs(Base):
    __tablename__ = "user_orgs"


    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    date_joined = Column(DateTime, default=datetime.utcnow())

