from sqlalchemy import Column, Integer, ForeignKey
from app.db.database import Base

class UserInterest(Base):
    __tablename__ = "user_interests"

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        primary_key=True
    )

    interest_id = Column(
        Integer,
        ForeignKey("interests.id"),
        primary_key=True
    )