from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.interest import Interest
from app.schemas.interest_schema import (
    InterestCreate,
    InterestResponse
)

router = APIRouter(tags=["Interests"])

@router.post(
    "/interests",
    response_model=InterestResponse
)
def create_interest(
    interest: InterestCreate,
    db: Session = Depends(get_db)
):
    existing = db.query(Interest).filter(
        Interest.name == interest.name
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Interest already exists"
        )

    new_interest = Interest(
        name=interest.name,
        category=interest.category
    )

    db.add(new_interest)
    db.commit()
    db.refresh(new_interest)

    return new_interest


@router.get(
    "/interests",
    response_model=List[InterestResponse]
)
def get_interests(
    db: Session = Depends(get_db)
):
    return db.query(Interest).all()