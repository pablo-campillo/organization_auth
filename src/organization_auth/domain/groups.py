from __future__ import annotations
from typing import List, Set

from pydantic import UUID4, Field

from organization_auth.domain.base import DCEBaseModel


class GroupUser(DCEBaseModel):
    team_id: UUID4
    group_id: UUID4
    role: str


class Group(DCEBaseModel):
    team_id: UUID4
    name: str
    role: str
    deleted: bool = False
    enabled: bool = True

    roles: Set[str] = Field(default_factory=set)
    users: List[GroupUser] = Field(default_factory=list)

    def __init__(self, **data):
        super().__init__(**data)
        self.roles.add(self.role)

    def is_valid_role(self, role_name: str):
        return role_name in self.roles

    def add_role(self, new_role_name: str) -> Group:
        self.roles.add(new_role_name)
        return self
