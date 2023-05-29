import uuid
from pynamodb.attributes import UnicodeAttribute, BooleanAttribute

from organization_auth.adapters.dynamodb.base import DDBOrganizationModel
from organization_auth.domain.users import User


USER_CLASS = "User"


class DDBUser(DDBOrganizationModel, discriminator=USER_CLASS):
    name = UnicodeAttribute()
    role = UnicodeAttribute()
    deleted = BooleanAttribute()
    enabled = BooleanAttribute()

    @staticmethod
    def from_domain(user: User):
        return DDBUser(
            str(user.team_id), f"{USER_CLASS}-{user.id}",
            name=user.name,
            role=user.role,
            deleted=user.deleted,
            enabled=user.enabled,
            created_at=user.created_at,
            updated_at=user.updated_at,
            )

    def to_domain(self):
        return User(
            id=uuid.UUID(str(self.sk_id)[len(USER_CLASS):]),
            team_id=uuid.UUID(self.pk_id),
            name=self.name,
            role=self.role,
            deleted=self.deleted,
            enabled=self.enabled,
            created_at=self.created_at,
            updated_at=self.updated_at,
            )
