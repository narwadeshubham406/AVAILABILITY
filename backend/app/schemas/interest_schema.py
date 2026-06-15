from pydantic import BaseModel

class InterestCreate(BaseModel):
    name: str
    category: str

class InterestResponse(BaseModel):
    id: int
    name: str
    category: str

    class Config:
        from_attributes = True