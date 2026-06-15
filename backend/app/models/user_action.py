from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.database import Base


class UserAction(Base):
    __tablename__ = "user_actions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    from_user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    to_user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    action = Column(String)