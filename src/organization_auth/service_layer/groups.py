from uuid import uuid4
from typing import List, Optional
from pydantic import UUID4
from organization_auth.adapters.repositories.teams import TeamsAbstractRepository
from organization_auth.domain.groups import Group
from organization_auth.domain.roles import DCERoleEnum

from organization_auth.service_layer.exceptions import (
    GroupAlreadyExistsException, GroupDoesNotExistException, RoleDoesNotExistException
)


def create_group(repo: TeamsAbstractRepository,
                 team_id: UUID4, name: str, role: str, group_id: Optional[UUID4] = None, 
                 roles: Optional[List] = []) -> Group:
    if group_id is None:
        group_id = uuid4()
    if (group := repo.get_group(group_id)) is not None:
        raise GroupAlreadyExistsException()
    group = Group(id=group_id, team_id=team_id, name=name, role=role, roles=roles)
    return repo.save_group(group)


def delete_group(repo: TeamsAbstractRepository, group_id: UUID4) -> Group:
    if (group := repo.get_group(group_id=group_id)) is not None:
        group.deleted = True
        return repo.save_group(group)
    else:
        raise GroupDoesNotExistException()


def disable_group(repo: TeamsAbstractRepository, group_id: UUID4) -> Group:
    if (group := repo.get_group(group_id=group_id)) is not None:
        group.enabled = False
        return repo.save_group(group)
    else:
        raise GroupDoesNotExistException()


def enable_group(repo: TeamsAbstractRepository, group_id: UUID4) -> Group:
    if (group := repo.get_group(group_id=group_id)) is not None:
        group.enabled = True
        return repo.save_group(group)
    else:
        raise GroupDoesNotExistException()


def change_group_name(repo: TeamsAbstractRepository, group_id: UUID4, new_name: str) -> Group:
    if (group := repo.get_group(group_id=group_id)) is not None:
        group.name = new_name
        return repo.save_group(group)
    else:
        raise GroupDoesNotExistException()


def change_group_role(repo: TeamsAbstractRepository, group_id: UUID4, new_role: str) -> Group:
    if not DCERoleEnum.is_valid(new_role):
        raise RoleDoesNotExistException()
    if (group := repo.get_group(group_id=group_id)) is not None:
        group.role = new_role
        return repo.save_group(group)
    else:
        raise GroupDoesNotExistException()


def get_group(repo: TeamsAbstractRepository, group_id: UUID4) -> Group:
    if (group := repo.get_group(group_id=group_id)) is not None:
        return group
    else:
        raise GroupDoesNotExistException()


def list_groups(repo: TeamsAbstractRepository, team_id: UUID4) -> List[Group]:
    return repo.list_groups(team_id)


def add_role(repo: TeamsAbstractRepository, group_id: UUID4, new_role_name: str) -> Group:
    if (group := repo.get_group(group_id=group_id)) is not None:
        updated_group = group.add_role(new_role_name)
        return repo.save_group(updated_group)
    else:
        raise GroupDoesNotExistException()
