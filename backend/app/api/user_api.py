from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.auth.dependencies import get_current_user

from app.db.session import get_db
from app.models.user import User
from app.schemas.user_schema import (
    UserCreate,
    UserResponse,
    UserLogin
)

from app.auth.hashing import (
    hash_password,
    verify_password
)

from app.auth.jwt_handler import create_access_token
from app.models.interest import Interest
from app.schemas.user_interest_schema import UserInterestAssign
router = APIRouter()

@router.post(
    "/signup",
    response_model=UserResponse
)
def signup(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    new_user = User(name=user.name,
                    email=user.email,
                    password=hash_password(user.password),
                    gender=user.gender,
                    age=user.age)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post("/login")
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not existing_user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if not verify_password(
        user.password,
        existing_user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid password"
        )

    access_token = create_access_token(
        data={
            "sub": existing_user.email
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get("/profile")
def profile(
    current_user: User = Depends(get_current_user)
):
    return {
    "message": "Protected Route Access Granted",
    "email": current_user.email,
    "name": current_user.name,
    "gender": current_user.gender,
    "age": current_user.age
    }

@router.post("/users/interests")
def assign_interests(
    data: UserInterestAssign,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    interests = db.query(Interest).filter(
        Interest.id.in_(data.interest_ids)
    ).all()

    current_user.interests = interests

    db.commit()

    return {
        "message": "Interests assigned successfully"
    }

@router.get("/users/interests")
def get_user_interests(
    current_user: User = Depends(get_current_user)
):
    return current_user.interests