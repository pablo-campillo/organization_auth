from typing import List

from pydantic import UUID4, Field

from organization_auth.domain.roles import DCERoleEnum
from organization_auth.domain.base import DCEBaseModel


class GroupUser(DCEBaseModel):
    team_id: UUID4
    group_id: UUID4
    role: DCERoleEnum


class Group(DCEBaseModel):
    team_id: UUID4
    name: str
    role: DCERoleEnum
    deleted: bool = False
    enabled: bool = True

    users: List[GroupUser] = Field(default_factory=list)

# claims del jwt token:
# {"user_id": "f34t3242564y", "groups": [{"group_id": "23242fqwef23r", "role": "User"}, {"group_id": "23242fqwef23r", "role": "Admin"}]}
