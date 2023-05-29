from typing import List
from pydantic import UUID4

from organization_auth.adapters.repositories.teams import TeamsAbstractRepository
from organization_auth.domain.groups import Group, GroupUser
from organization_auth.service_layer.exceptions import (
    GroupUserDoesNotExistException, RoleDoesNotExistException, UserAlreadyInGroupException
)
from organization_auth.service_layer.groups import get_group
from organization_auth.service_layer.users import get_user


def is_user_in_group(repo: TeamsAbstractRepository, team_id: UUID4, group_id: UUID4, user_id: UUID4) -> bool:
    return repo.is_user_in_group(team_id, group_id, user_id)


def get_user_in_group(repo: TeamsAbstractRepository, team_id: UUID4, group_id: UUID4, user_id: UUID4) -> GroupUser:
    return repo.get_user_in_group(team_id, group_id, user_id)


def add_user_to_group(repo: TeamsAbstractRepository, group_id: UUID4, user_id: UUID4,
                      role: str) -> GroupUser:
    user = get_user(repo, user_id)
    group = get_group(repo, group_id)
    team_id = group.team_id

    if is_user_in_group(repo, team_id, group_id, user_id):
        raise UserAlreadyInGroupException()

    if not group.is_valid_role(role_name=role):
        raise RoleDoesNotExistException()

    group_user = GroupUser(id=user.id, team_id=team_id, group_id=group.id, role=role)
    return repo.save_group_user(group_user)


def change_user_group_role(repo: TeamsAbstractRepository, team_id: UUID4, group_id: UUID4, user_id: UUID4,
                           new_role: str) -> GroupUser:
    group = get_group(repo, group_id)

    if not group.is_valid_role(role_name=new_role):
        raise RoleDoesNotExistException()

    if (group_user := get_user_in_group(repo, team_id, group_id, user_id)) is not None:
        print(group_user)
        group_user.role = new_role
        result = repo.save_group_user(group_user)
        print(result)
        return result
    else:
        raise GroupUserDoesNotExistException()


# def delete_user_from_group(repo: TeamsAbstractRepository,
#                            team_id: UUID4, group_id: UUID4, user_id: UUID4) -> GroupUser:
#     if (group_user := get_user_in_group(repo, team_id, group_id, user_id)) is not None:
#         group_user.role = new_role
#         return repo.save_group_user(group_user)
#     else:
#         raise GroupUserDoesNotExist()


def list_group_users(repo: TeamsAbstractRepository, team_id: UUID4, group_id: UUID4) -> List[GroupUser]:
    return repo.list_group_users(team_id=team_id, group_id=group_id)


def list_groups_of_user(repo: TeamsAbstractRepository, team_id: UUID4, user_id: UUID4) -> List[GroupUser]:
    return repo.list_groups_of_user(team_id=team_id, user_id=user_id)