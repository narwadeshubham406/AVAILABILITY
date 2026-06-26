from sqlalchemy import (
    Column,
    Integer,
    Date,
    String,
    ForeignKey
)

from sqlalchemy.orm import relationship

from app.db.database import Base


class AvailabilitySlot(Base):
    __tablename__ = "availability_slots"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    available_date = Column(
        Date,
        nullable=False
    )

    start_time = Column(
        String,
        nullable=False
    )

    end_time = Column(
        String,
        nullable=False
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    user = relationship(
        "User",
        back_populates="availability_slots"
    )