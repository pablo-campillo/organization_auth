from datetime import datetime
from typing import List
from pydantic import UUID4, BaseModel


class GroupUserInfo(BaseModel):
    group_id: UUID4
    role: str


class UserToken(BaseModel):
    exp: datetime
    team_id: UUID4
    user_id: UUID4
    groups: List[GroupUserInfo]
