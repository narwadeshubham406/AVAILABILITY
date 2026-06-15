from pydantic import BaseModel


class AvailabilityCreate(BaseModel):
    day: str
    start_time: str
    end_time: str


class AvailabilityResponse(BaseModel):
    id: int
    day: str
    start_time: str
    end_time: str

    class Config:
        from_attributes = True