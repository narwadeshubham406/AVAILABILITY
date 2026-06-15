from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.database import Base


class UserPreference(Base):
    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        unique=True
    )

    preferred_gender = Column(String)
    language = Column(String)
    city = Column(String)

    age_min = Column(Integer)
    age_max = Column(Integer)

    user = relationship(
        "User",
        back_populates="preference"
    )