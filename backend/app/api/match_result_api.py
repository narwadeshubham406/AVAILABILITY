from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.db.session import get_db
from app.auth.dependencies import get_current_user

from app.models.user import User
from app.models.match import Match

router = APIRouter(tags=["My Matches"])


@router.get("/my-matches")
def get_my_matches(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    matches = db.query(Match).filter(
        or_(
            Match.user1_id == current_user.id,
            Match.user2_id == current_user.id
        )
    ).all()

    result = []

    for match in matches:

        if match.user1_id == current_user.id:
            other_user = db.query(User).filter(
                User.id == match.user2_id
            ).first()
        else:
            other_user = db.query(User).filter(
                User.id == match.user1_id
            ).first()

        result.append({
            "user_id": other_user.id,
            "name": other_user.name
        })

    return result