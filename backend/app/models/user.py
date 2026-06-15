from sqlalchemy import Column, Integer, String
from app.db.database import Base
from sqlalchemy.orm import relationship
from app.models.user_interest import UserInterest
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String,unique=True,nullable=False)
    password = Column(String,nullable=False)
    gender = Column(String,nullable=True)
    age = Column(Integer,nullable=True)	


    interests = relationship(
    "Interest",
    secondary=UserInterest.__table__,
    back_populates="users"
    )

    availability_slots = relationship(
    "AvailabilitySlot",
    back_populates="user",
    cascade="all, delete-orphan"
    )

    preference = relationship(
    "UserPreference",
    back_populates="user",
    uselist=False,
    cascade="all, delete-orphan"
    )