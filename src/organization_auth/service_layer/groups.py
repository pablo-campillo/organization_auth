from uuid import uuid4
from typing import List, Optional
from pydantic import UUID4
from organization_auth.adapters.repositories.teams import TeamsAbstractRepository
from organization_auth.domain.groups import Group
from organization_auth.domain.roles import DCERoleEnum

from organization_auth.service_layer.exceptions import (
    GroupAlreadyExists, GroupDoesNotExist, RoleDoesNotExist
)


def create_group(repo: TeamsAbstractRepository,
                 team_id: UUID4, name: str, role: str, group_id: Optional[UUID4] = None) -> Group:
    if group_id is None:
        group_id = uuid4()
    if (group := repo.get_group(group_id)) is not None:
        raise GroupAlreadyExists()
    group = Group(id=group_id, team_id=team_id, name=name, role=role)
    return repo.save_group(group)


def delete_group(repo: TeamsAbstractRepository, group_id: UUID4) -> Group:
    if (group := repo.get_group(group_id=group_id)) is not None:
        group.deleted = True
        return repo.save_group(group)
    else:
        raise GroupDoesNotExist()


def disable_group(repo: TeamsAbstractRepository, group_id: UUID4) -> Group:
    if (group := repo.get_group(group_id=group_id)) is not None:
        group.enabled = False
        return repo.save_group(group)
    else:
        raise GroupDoesNotExist()


def enable_group(repo: TeamsAbstractRepository, group_id: UUID4) -> Group:
    if (group := repo.get_group(group_id=group_id)) is not None:
        group.enabled = True
        return repo.save_group(group)
    else:
        raise GroupDoesNotExist()


def change_group_name(repo: TeamsAbstractRepository, group_id: UUID4, new_name: str) -> Group:
    if (group := repo.get_group(group_id=group_id)) is not None:
        group.name = new_name
        return repo.save_group(group)
    else:
        raise GroupDoesNotExist()


def change_group_role(repo: TeamsAbstractRepository, group_id: UUID4, new_role: str) -> Group:
    if not DCERoleEnum.is_valid(new_role):
        raise RoleDoesNotExist()
    if (group := repo.get_group(group_id=group_id)) is not None:
        group.role = new_role
        return repo.save_group(group)
    else:
        raise GroupDoesNotExist()


def get_group(repo: TeamsAbstractRepository, group_id: UUID4) -> Group:
    if (group := repo.get_group(group_id=group_id)) is not None:
        return group
    else:
        raise GroupDoesNotExist()


def list_groups(repo: TeamsAbstractRepository, team_id: UUID4) -> List[Group]:
    return repo.list_groups(team_id)
