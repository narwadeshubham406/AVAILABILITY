from pydantic import BaseModel


class MatchResponse(BaseModel):
    user_id: int
    name: str

    class Config:
        from_attributes = True