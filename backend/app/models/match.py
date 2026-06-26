# app/models/match.py

from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    DateTime
)

from datetime import datetime

from app.db.database import Base


class Match(Base):
    __tablename__ = "matches"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user1_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    user2_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )