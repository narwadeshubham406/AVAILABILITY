from fastapi import FastAPI
from app.db.database import Base, engine
from app.models.user import User
from app.api.user_api import router as user_router
from app.models.interest import Interest
from app.api.interest_api import router as interest_router
from app.models.availability import AvailabilitySlot
from app.api.availability_api import router as availability_router
from app.models.user_interest import UserInterest
from app.models.user_preference import UserPreference
from app.api.preference_api import router as preference_router
from app.api.match_api import router as match_router
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user_router)
app.include_router(interest_router)
app.include_router(availability_router)
app.include_router(preference_router)
app.include_router(match_router)
@app.get("/")
def home():
    return {
        "message": "AVAILABILITY API Running Successfully"
    }