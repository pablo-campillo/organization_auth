from pydantic import UUID4

from organization_auth.domain.base import DCEBaseModel


class User(DCEBaseModel):
    team_id: UUID4
    name: str
    role: str
    deleted: bool = False
    enabled: bool = True
