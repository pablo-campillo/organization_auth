import pytest
from organization_auth.service_layer.exceptions import (
    GroupDoesNotExistException, GroupUserDoesNotExistException, RoleDoesNotExistException,
    UserAlreadyInGroupException, UserDoesNotExistException
)
from organization_auth.service_layer.group_user import (
    add_user_to_group, change_user_group_role, list_group_users, list_groups_of_user
)


def test_add_user_to_group(repo, team_with_a_user_and_empty_group):
    team = team_with_a_user_and_empty_group
    group_id = team.groups[0].id
    user_id = team.users[0].id
    role = "User"
    group_user = add_user_to_group(repo, group_id=group_id, user_id=user_id, role=role)

    assert group_user.id == user_id
    assert group_user.team_id == team.id
    assert group_user.group_id == group_id
    assert group_user.role == role


def test_add_user_to_group_where_group_does_not_exists(repo, team_with_a_user_and_empty_group):
    team = team_with_a_user_and_empty_group
    user_id = team.users[0].id
    role = "User"

    with pytest.raises(GroupDoesNotExistException):
        add_user_to_group(repo, group_id="Fake", user_id=user_id, role=role)


def test_add_user_to_group_where_user_does_not_exists(repo, team_with_a_user_and_empty_group):
    team = team_with_a_user_and_empty_group
    group_id = team.groups[0].id
    user_id = "Fake"
    role = "User"

    with pytest.raises(UserDoesNotExistException):
        add_user_to_group(repo, group_id=group_id, user_id=user_id, role=role)


def test_add_user_to_group_where_user_already_in_group(repo, user_in_group):
    group_id = user_in_group.group_id
    user_id = user_in_group.id
    role = "User"

    with pytest.raises(UserAlreadyInGroupException):
        add_user_to_group(repo, group_id=group_id, user_id=user_id, role=role)


def test_add_user_to_group_where_role_does_not_exist(repo, team_with_a_user_and_empty_group):
    team = team_with_a_user_and_empty_group
    group_id = team.groups[0].id
    user_id = team.users[0].id
    role = "Fake"

    with pytest.raises(RoleDoesNotExistException):
        add_user_to_group(repo, group_id=group_id, user_id=user_id, role=role)


def test_change_user_group_role(repo, user_in_group):
    new_role = "Power_User"
    updated_at = user_in_group.updated_at
    group_user = change_user_group_role(repo, team_id=user_in_group.team_id,
                                        group_id=user_in_group.group_id, user_id=user_in_group.id, new_role=new_role)

    assert group_user.role == new_role
    assert updated_at < group_user.updated_at


def test_change_user_group_role_does_not_exists(repo, user_in_group):
    new_role = "Fake"
    with pytest.raises(RoleDoesNotExistException):
        change_user_group_role(repo, team_id=user_in_group.team_id,
                               group_id=user_in_group.group_id, user_id=user_in_group.id, new_role=new_role)


def test_change_user_group_role_where_user_does_not_exist(repo, user_in_group):
    new_role = "Power_User"
    user_id = "Fake"
    group_id = user_in_group.group_id

    with pytest.raises(GroupUserDoesNotExistException):
        change_user_group_role(repo, team_id=user_in_group.team_id,
                               group_id=group_id, user_id=user_id, new_role=new_role)


def test_list_group_users(repo, team_with_user_in_3_groups):
    team = team_with_user_in_3_groups
    group_users = list_group_users(repo, team.id, team.groups[0].id)

    assert len(group_users) == 2


def test_list_groups_of_user(repo, team_with_user_in_3_groups):
    team = team_with_user_in_3_groups
    groups = list_groups_of_user(repo, team.id, team.users[0].id)

    assert len(groups) == 3
