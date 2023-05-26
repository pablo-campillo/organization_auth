import uuid
from pynamodb.attributes import UnicodeAttribute, BooleanAttribute

from organization_auth.adapters.dynamodb.base import DDBOrganizationModel
from organization_auth.domain.groups import Group, GroupUser


GROUP_CLASS = "Group"


class DDBGroup(DDBOrganizationModel, discriminator=GROUP_CLASS):
    name = UnicodeAttribute()
    role = UnicodeAttribute()
    deleted = BooleanAttribute()
    enabled = BooleanAttribute()

    @staticmethod
    def from_domain(group: Group):
        return DDBGroup(
            str(group.team_id), f"{GROUP_CLASS}-{group.id}",
            name=group.name,
            role=group.role,
            deleted=group.deleted,
            enabled=group.enabled,
            created_at=group.created_at,
            updated_at=group.updated_at,
            )

    def to_domain(self):
        return Group(
            id=uuid.UUID(str(self.sk_id)[len(GROUP_CLASS):]),
            team_id=uuid.UUID(self.pk_id),
            name=self.name,
            role=self.role,
            deleted=self.deleted,
            enabled=self.enabled,
            created_at=self.created_at,
            updated_at=self.updated_at,
            )


GROUP_USER_CLASS = "GroupUser"


class DDBGroupUser(DDBOrganizationModel, discriminator=GROUP_USER_CLASS):
    role = UnicodeAttribute()

    @staticmethod
    def from_domain(group_user: GroupUser):
        return DDBGroupUser(
            str(group_user.team_id), f"{group_user.group_id}#{group_user.id}",
            role=group_user.role,
            created_at=group_user.created_at,
            updated_at=group_user.updated_at,
            )

    def to_domain(self):
        group_id, user_id = self.sk_id.split('#')
        return GroupUser(
            id=user_id,
            team_id=uuid.UUID(self.pk_id),
            group_id=group_id,
            role=self.role,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
