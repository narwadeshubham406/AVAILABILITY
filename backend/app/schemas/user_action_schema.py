from pydantic import BaseModel


class UserActionCreate(BaseModel):
    to_user_id: int
    action: str