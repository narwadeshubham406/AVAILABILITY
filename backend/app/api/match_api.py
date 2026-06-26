from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.auth.dependencies import get_current_user

from app.models.user import User
from app.models.user_action import UserAction

from app.services.match_service import (
    calculate_match_score,
    get_match_reasons,
    passes_mutual_preference_filter
)

router = APIRouter(tags=["Matches"])


@router.get("/matches")
def get_matches(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    users = db.query(User).all()

    # Users already liked/passed
    seen_user_ids = {
        action.to_user_id
        for action in db.query(UserAction)
        .filter(
            UserAction.from_user_id
            ==
            current_user.id
        )
        .all()
    }

    matches = []

    for user in users:

        # Skip yourself
        if user.id == current_user.id:
            continue

        # Skip already seen users
        if user.id in seen_user_ids:
            continue

        # Apply mutual preference filter
        if not passes_mutual_preference_filter(
            current_user,
            user
        ):
            continue

        score = calculate_match_score(
            current_user,
            user
        )

        matches.append({
            "user_id": user.id,
            "name": user.name,
            "score": score,
            "reasons": get_match_reasons(
                current_user,
                user
            )
        })

    matches.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return matches