from pydantic import BaseModel
from typing import List

class UserInterestAssign(BaseModel):
    interest_ids: List[int]