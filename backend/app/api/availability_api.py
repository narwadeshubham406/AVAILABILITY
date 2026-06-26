from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.auth.dependencies import get_current_user

from app.models.user import User
from app.models.availability import AvailabilitySlot

from app.schemas.availability_schema import (
    AvailabilityCreate,
    AvailabilityResponse
)

router = APIRouter(tags=["Availability"])


@router.post(
    "/availability",
    response_model=AvailabilityResponse
)
def create_availability(
    data: AvailabilityCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    slot = AvailabilitySlot(
        available_date=data.available_date,
        start_time=data.start_time,
        end_time=data.end_time,
        user_id=current_user.id
    )

    db.add(slot)
    db.commit()
    db.refresh(slot)

    return slot


@router.get(
    "/availability",
    response_model=list[AvailabilityResponse]
)
def get_availability(
    current_user: User = Depends(get_current_user)
):

    return current_user.availability_slots


@router.delete("/availability/{slot_id}")
def delete_slot(
    slot_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    slot = db.query(AvailabilitySlot).filter(
        AvailabilitySlot.id == slot_id,
        AvailabilitySlot.user_id == current_user.id
    ).first()

    if slot:
        db.delete(slot)
        db.commit()

    return {
        "message": "Slot deleted"
    }