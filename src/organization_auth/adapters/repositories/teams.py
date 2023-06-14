import abc
from typing import List
from organization_auth.adapters.dynamodb.base import DDBOrganizationModel
from organization_auth.domain.base import DCEBaseModel

from pydantic import UUID4
from organization_auth.adapters.dynamodb.groups import GROUP_CLASS, DDBGroup, DDBGroupUser
from organization_auth.adapters.dynamodb.teams import TEAM_CLASS, DDBTeam
from organization_auth.adapters.dynamodb.users import USER_CLASS, DDBUser
from organization_auth.domain.groups import Group, GroupUser

from organization_auth.domain.teams import Team
from organization_auth.domain.users import User


class TeamsAbstractRepository(abc.ABC):

    @abc.abstractmethod
    def save_team(self, team: Team) -> Team:  # pragma: no cover
        pass

    @abc.abstractmethod
    def get_team(self, id: UUID4) -> Team:  # pragma: no cover
        pass

    @abc.abstractmethod
    def list_teams(self) -> List[Team]:  # pragma: no cover
        pass

    @abc.abstractmethod
    def save_group(self, group: Group) -> Group:  # pragma: no cover
        pass

    @abc.abstractmethod
    def get_group(self, group_id: UUID4) -> Group:  # pragma: no cover
        pass

    @abc.abstractmethod
    def list_groups(self, team_id: UUID4) -> List[Group]:  # pragma: no cover
        pass

    @abc.abstractmethod
    def save_user(self, user: User) -> User:  # pragma: no cover
        pass

    @abc.abstractmethod
    def get_user(self, user_id: UUID4):  # pragma: no cover
        pass

    @abc.abstractmethod
    def list_users(self, team_id: UUID4):  # pragma: no cover
        pass

    @abc.abstractmethod
    def is_user_in_group(self, team_id: UUID4, group_id: UUID4, user_id: UUID4) -> bool:  # pragma: no cover
        pass

    @abc.abstractmethod
    def get_user_in_group(self, team_id: UUID4, group_id: UUID4, user_id: UUID4) -> GroupUser:  # pragma: no cover
        pass

    @abc.abstractmethod
    def save_group_user(self, group_user: GroupUser) -> GroupUser:  # pragma: no cover
        pass

    @abc.abstractmethod
    def list_group_users(self, team_id: UUID4, group_id: UUID4) -> List[GroupUser]:  # pragma: no cover
        pass

    @abc.abstractmethod
    def list_groups_of_user(self, team_id: UUID4, user_id: UUID4) -> List[Group]:  # pragma: no cover
        pass

    def list_all(self) -> List[DCEBaseModel]:  # pragma: no cover
        pass


class TeamsDynamoDBRepository(TeamsAbstractRepository):
    def save_team(self, team: Team) -> Team:
        ddb_team = DDBTeam.from_domain(team)
        ddb_team.save()
        return ddb_team.to_domain()

    def get_team(self, id: UUID4) -> Team:
        try:
            ddb_team = DDBTeam.get(str(id), TEAM_CLASS)
            return ddb_team.to_domain()
        except DDBTeam.DoesNotExist:
            pass

    def list_teams(self) -> List[Team]:
        return [
            ddb_team.to_domain()
            for ddb_team in DDBTeam.classes_index.query(TEAM_CLASS)
        ]

    def save_group(self, group: Group) -> Group:
        ddb_group = DDBGroup.from_domain(group)
        ddb_group.save()
        return ddb_group.to_domain()

    def get_group(self, group_id: UUID4) -> Group:
        try:
            ddb_group = next(DDBGroup.classes_index.query(f"{GROUP_CLASS}-{group_id}"))
            return ddb_group.to_domain()
        except StopIteration:
            pass

    def list_groups(self, team_id: UUID4):
        return [
            ddb_group.to_domain()
            for ddb_group in DDBGroup.query(str(team_id), DDBGroup.sk_id.startswith(f"{GROUP_CLASS}-"))
        ]

    def save_user(self, user: User) -> User:
        ddb_user = DDBUser.from_domain(user)
        ddb_user.save()
        return ddb_user.to_domain()

    def get_user(self, user_id: UUID4):
        try:
            ddb_user = next(DDBUser.classes_index.query(f"{USER_CLASS}-{user_id}"))
            return ddb_user.to_domain()
        except StopIteration:
            pass

    def list_users(self, team_id: UUID4):
        return [
            ddb_user.to_domain()
            for ddb_user in DDBUser.query(str(team_id), DDBUser.sk_id.startswith(f"{USER_CLASS}-"))
        ]

    def is_user_in_group(self, team_id: UUID4, group_id: UUID4, user_id: UUID4) -> bool:
        return self.get_user_in_group(team_id, group_id, user_id) is not None

    def get_user_in_group(self, team_id: UUID4, group_id: UUID4, user_id: UUID4) -> GroupUser:
        try:
            ddb_group_user = DDBGroupUser.get(str(team_id), f"{group_id}#{user_id}")
            return ddb_group_user.to_domain()
        except DDBGroupUser.DoesNotExist:
            pass

    def save_group_user(self, group_user: GroupUser) -> GroupUser:
        ddb_group_user = DDBGroupUser.from_domain(group_user)
        ddb_group_user.save()
        return ddb_group_user.to_domain()

    def list_group_users(self, team_id: UUID4, group_id: UUID4) -> List[GroupUser]:  # pragma: no cover
        return [
            ddb_group_user.to_domain()
            for ddb_group_user in DDBGroupUser.query(str(team_id),
                                                     DDBGroupUser.sk_id.startswith(f"{group_id}#"))
        ]

    def list_groups_of_user(self, team_id: UUID4, user_id: UUID4) -> List[Group]:
        return [
            ddb_group.to_domain()
            for ddb_group in DDBGroupUser.scan(
                                                (DDBGroupUser.pk_id == str(team_id)) &
                                                (DDBGroupUser.sk_id.contains(f"#{user_id}"))
                                                )
        ]

    def list_all(self) -> List[DCEBaseModel]:
        return [
            ddb_item.to_domain()
            for ddb_item in DDBOrganizationModel.scan()
        ]

    def save_all(self, items: List[DCEBaseModel]) -> List[DCEBaseModel]:

        with DDBOrganizationModel.batch_write() as batch:
            for item in items:
                if isinstance(item, Team):
                    batch.save(DDBTeam.from_domain(item))
                elif isinstance(item, Group):
                    batch.save(DDBGroup.from_domain(item))
                if isinstance(item, User):
                    batch.save(DDBUser.from_domain(item))
                if isinstance(item, GroupUser):
                    batch.save(DDBGroupUser.from_domain(item))

        return items
