from pydantic import BaseModel


class UserPreferenceCreate(BaseModel):
    preferred_gender: str
    language: str
    city: str
    age_min: int
    age_max: int