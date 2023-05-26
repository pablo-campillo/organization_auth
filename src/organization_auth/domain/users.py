from pydantic import UUID4

from organization_auth.domain.roles import DCERoleEnum
from organization_auth.domain.base import DCEBaseModel


class User(DCEBaseModel):
    team_id: UUID4
    name: str
    role: DCERoleEnum
    deleted: bool = False
    enabled: bool = True
