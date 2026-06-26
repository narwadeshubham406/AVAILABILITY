from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.auth.dependencies import get_current_user

from app.models.user import User
from app.models.user_action import UserAction
from app.models.match import Match

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

    # Save current action
    action = UserAction(
        from_user_id=current_user.id,
        to_user_id=data.to_user_id,
        action=data.action
    )

    db.add(action)
    db.commit()

    # Only check mutual match for likes
    if data.action == "like":

        reverse_like = db.query(UserAction).filter(
            UserAction.from_user_id == data.to_user_id,
            UserAction.to_user_id == current_user.id,
            UserAction.action == "like"
        ).first()

        if reverse_like:

            user1 = min(
                current_user.id,
                data.to_user_id
            )

            user2 = max(
                current_user.id,
                data.to_user_id
            )

            existing_match = db.query(Match).filter(
                Match.user1_id == user1,
                Match.user2_id == user2
            ).first()

            if not existing_match:

                match = Match(
                    user1_id=user1,
                    user2_id=user2
                )

                db.add(match)
                db.commit()

                return {
                    "message": "It's a Match!"
                }

    return {
        "message": "Action saved"
    }