from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.auth.dependencies import get_current_user

from app.models.user import User
from app.models.user_preference import UserPreference

from app.schemas.user_preference_schema import (
    UserPreferenceCreate
)

router = APIRouter(tags=["Preferences"])


@router.post("/preferences")
def create_preference(
    data: UserPreferenceCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    preference = UserPreference(
        user_id=current_user.id,
        preferred_gender=data.preferred_gender,
        language=data.language,
        city=data.city,
        age_min=data.age_min,
        age_max=data.age_max
    )

    db.add(preference)
    db.commit()
    db.refresh(preference)

    return preference


@router.get("/preferences")
def get_preference(
    current_user: User = Depends(get_current_user)
):
    return current_user.preference