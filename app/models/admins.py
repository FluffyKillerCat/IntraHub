from sqlalchemy import Integer, String, Column, ForeignKey
from app.db.base import Base


class Admins(Base):
    __tablename__ = 'admins'  # Corrected this line

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    org_id = Column(Integer, ForeignKey('organizations.id'), nullable=True)
    accepted_by = Column(String, ForeignKey('users.username'))
    status = Column(String(50), nullable=True, comment="e.g., pending, approved, attended, declined", default="approved")
