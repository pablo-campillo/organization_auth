
from uuid import uuid4, UUID
import pytest
from organization_auth.adapters.repositories.teams import TeamsDynamoDBRepository

from organization_auth.domain.teams import Team
from organization_auth.domain.users import User
from organization_auth.service_layer.exceptions import (
    RoleDoesNotExistException, TeamDoesNotExistException, UserAlreadyExistsException, UserDoesNotExistException
)
from organization_auth.service_layer.users import (
    change_user_name, change_user_role, create_user, delete_user, disable_user, enable_user, list_users
)


def test_create_user(repo: TeamsDynamoDBRepository, empty_team: Team):
    user_id = uuid4()
    name = "MyUser"
    role = "User"
    user = create_user(repo, team_id=empty_team.id, user_id=user_id, name=name, role=role)

    assert user.id == user_id
    assert user.team_id == empty_team.id
    assert user.name == name
    assert user.enabled
    assert not user.deleted


def test_create_user_team_does_not_exist(repo: TeamsDynamoDBRepository, empty_user: User):
    role = "User"
    name = "MyUser"
    team_id = "Fake"

    with pytest.raises(TeamDoesNotExistException):
        create_user(repo, team_id=team_id, name=name, role=role)


def test_create_user_with_auto_id(repo: TeamsDynamoDBRepository, empty_team: Team):
    name = "MyUser"
    role = "User"
    user = create_user(repo, team_id=empty_team.id, name=name, role=role)

    assert isinstance(user.id, UUID)
    assert user.team_id == empty_team.id
    assert user.name == name
    assert user.enabled
    assert not user.deleted


def test_create_user_already_exists(repo: TeamsDynamoDBRepository, empty_user: User):
    role = "User"
    name = "MyUser"

    with pytest.raises(UserAlreadyExistsException):
        create_user(repo, team_id=empty_user.team_id, user_id=empty_user.id, name=name, role=role)


def test_delete_user(repo: TeamsDynamoDBRepository, empty_user: User):
    team = delete_user(repo, user_id=empty_user.id)

    assert team.deleted


def test_delete_user_does_not_exists(repo: TeamsDynamoDBRepository):
    with pytest.raises(UserDoesNotExistException):
        delete_user(repo, user_id="Fake")


def test_disable_user(repo: TeamsDynamoDBRepository, empty_user: User):
    user = disable_user(repo, user_id=empty_user.id)

    assert not user.enabled


def test_diable_user_does_not_exists(repo: TeamsDynamoDBRepository):
    with pytest.raises(UserDoesNotExistException):
        disable_user(repo, user_id="Fake")


def test_enable_user(repo: TeamsDynamoDBRepository, empty_user: User):
    user = enable_user(repo, user_id=empty_user.id)

    assert user.enabled


def test_enable_user_does_not_exists(repo: TeamsDynamoDBRepository):
    with pytest.raises(UserDoesNotExistException):
        enable_user(repo, user_id="Fake")


def test_change_user_name(repo: TeamsDynamoDBRepository, empty_user: User):
    new_name = "MyNewUserName"
    updated_at = empty_user.updated_at
    user = change_user_name(repo, user_id=empty_user.id, new_name=new_name)

    assert user.name == new_name
    assert updated_at < user.updated_at


def test_change_user_name_does_not_exists(repo: TeamsDynamoDBRepository):
    new_name = "MyNewUserName"
    with pytest.raises(UserDoesNotExistException):
        change_user_name(repo, user_id="Fake", new_name=new_name)


def test_change_user_role(repo: TeamsDynamoDBRepository, empty_user: User):
    new_role = 'Team_Owner'
    updated_at = empty_user.updated_at
    user = change_user_role(repo, user_id=empty_user.id, new_role=new_role)

    assert user.role == new_role
    assert updated_at < user.updated_at


def test_change_user_role_does_not_exists(repo: TeamsDynamoDBRepository):
    new_role = 'Team_Owner'
    with pytest.raises(UserDoesNotExistException):
        change_user_role(repo, user_id="Fake", new_role=new_role)


def test_list_users(repo: TeamsDynamoDBRepository, team_with_5_users):
    users = list_users(repo, team_id=team_with_5_users.id)

    assert len(users) == 5
