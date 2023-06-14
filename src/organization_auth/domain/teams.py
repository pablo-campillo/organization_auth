from typing import List, Union
from pydantic import Field, UUID4

from organization_auth.domain.base import DCEBaseModel
from organization_auth.domain.users import User
from organization_auth.domain.groups import Group


class Team(DCEBaseModel):
    name: str
    deleted: bool = False
    enabled: bool = True

    users: List[User] = Field(default_factory=list)
    groups: List[Group] = Field(default_factory=list)

    def get_user(self, user_id: UUID4) -> Union[User, None]:
        for user in self.users:
            if user.id == user_id:
                return user
        return None
