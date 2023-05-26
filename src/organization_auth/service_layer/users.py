from uuid import uuid4
from typing import List, Optional
from pydantic import UUID4

from organization_auth.adapters.repositories.teams import TeamsAbstractRepository
from organization_auth.domain.roles import DCERoleEnum
from organization_auth.domain.users import User
from organization_auth.service_layer.exceptions import (
    RoleDoesNotExistException, UserAlreadyExistsException, UserDoesNotExistException
)


def create_user(repo: TeamsAbstractRepository, team_id: UUID4, name: str, role: str,
                user_id: Optional[UUID4] = None) -> User:
    if user_id is None:
        user_id = uuid4()
    else:
        # TODO Check if the user is already created in other Team
        pass

    if (user := repo.get_user(user_id)) is not None:
        raise UserAlreadyExistsException()
    user = User(id=user_id, team_id=team_id, name=name, role=role)
    return repo.save_user(user)


def get_user(repo: TeamsAbstractRepository, user_id: UUID4) -> User:
    if (user := repo.get_user(user_id=user_id)) is not None:
        return user
    else:
        raise UserDoesNotExistException()


def delete_user(repo: TeamsAbstractRepository, user_id: UUID4) -> User:
    if (user := repo.get_user(user_id=user_id)) is not None:
        user.deleted = True
        return repo.save_user(user)
    else:
        raise UserDoesNotExistException()


def disable_user(repo: TeamsAbstractRepository, user_id: UUID4) -> User:
    if (user := repo.get_user(user_id=user_id)) is not None:
        user.enabled = False
        return repo.save_user(user)
    else:
        raise UserDoesNotExistException()


def enable_user(repo: TeamsAbstractRepository, user_id: UUID4) -> User:
    if (user := repo.get_user(user_id=user_id)) is not None:
        user.enabled = True
        return repo.save_user(user)
    else:
        raise UserDoesNotExistException()


def change_user_name(repo: TeamsAbstractRepository, user_id: UUID4, new_name: str) -> User:
    if (user := repo.get_user(user_id=user_id)) is not None:
        user.name = new_name
        return repo.save_user(user)
    else:
        raise UserDoesNotExistException()


def change_user_role(repo: TeamsAbstractRepository, user_id: UUID4, new_role: str) -> User:
    if not DCERoleEnum.is_valid(new_role):
        raise RoleDoesNotExistException()
    if (user := repo.get_user(user_id=user_id)) is not None:
        user.role = new_role
        return repo.save_user(user)
    else:
        raise UserDoesNotExistException()


def list_users(repo: TeamsAbstractRepository, team_id: UUID4) -> List[User]:
    return repo.list_users(team_id)
