from pydantic import BaseModel
from datetime import date


class AvailabilityCreate(BaseModel):
    available_date: date
    start_time: str
    end_time: str


class AvailabilityResponse(BaseModel):
    id: int
    available_date: date
    start_time: str
    end_time: str

    class Config:
        from_attributes = True