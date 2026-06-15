from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.auth.dependencies import get_current_user

from app.models.user import User
from app.models.user_action import UserAction

from app.schemas.user_action_schema import (
    UserActionCreate
)

router = APIRouter(tags=["Actions"])


@router.post("/actions")
def create_action(
    data: UserActionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    action = UserAction(
        from_user_id=current_user.id,
        to_user_id=data.to_user_id,
        action=data.action
    )

    db.add(action)
    db.commit()

    return {
        "message": "Action saved"
    }