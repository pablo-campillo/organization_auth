import uuid
from pynamodb.attributes import UnicodeAttribute, BooleanAttribute

from organization_auth.adapters.dynamodb.base import DDBOrganizationModel
from organization_auth.domain.teams import Team

TEAM_CLASS = "Team"


class DDBTeam(DDBOrganizationModel, discriminator=TEAM_CLASS):
    name = UnicodeAttribute()
    deleted = BooleanAttribute()
    enabled = BooleanAttribute()

    @staticmethod
    def from_domain(team: Team):
        return DDBTeam(
            str(team.id), TEAM_CLASS,
            name=team.name,
            deleted=team.deleted,
            enabled=team.enabled,
            created_at=team.created_at,
            updated_at=team.updated_at,
            )

    def to_domain(self):
        return Team(
            id=uuid.UUID(self.pk_id),
            name=self.name,
            deleted=self.deleted,
            enabled=self.enabled,
            created_at=self.created_at,
            updated_at=self.updated_at,
            )

