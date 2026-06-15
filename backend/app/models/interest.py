from sqlalchemy import Column, Integer, String
from app.db.database import Base
from sqlalchemy.orm import relationship
from app.models.user_interest import UserInterest

class Interest(Base):
    __tablename__ = "interests"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    category = Column(String, nullable=False)

    users = relationship(
    "User",
    secondary=UserInterest.__table__,
    back_populates="interests"
    )