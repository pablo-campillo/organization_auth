import pytest
from organization_auth.domain.roles import DCERoleEnum
from organization_auth.service_layer.exceptions import (
    GroupDoesNotExist, GroupUserDoesNotExist, RoleDoesNotExist, UserAlreadyInGroup, UserDoesNotExist
)
from organization_auth.service_layer.group_user import (
    add_user_to_group, change_user_group_role, list_group_users, list_groups_of_user
)


def test_add_user_to_group(repo, team_with_a_user_and_empty_team):
    team = team_with_a_user_and_empty_team
    group_id = team.groups[0].id
    user_id = team.users[0].id
    role = DCERoleEnum.User.name
    group_user = add_user_to_group(repo, team_id=team.id, group_id=group_id, user_id=user_id, role=role)

    assert group_user.id == user_id
    assert group_user.team_id == team.id
    assert group_user.group_id == group_id
    assert group_user.role == role


def test_add_user_to_group_where_group_does_not_exists(repo, team_with_a_user_and_empty_team):
    team = team_with_a_user_and_empty_team
    user_id = team.users[0].id
    role = DCERoleEnum.User.name

    with pytest.raises(GroupDoesNotExist):
        add_user_to_group(repo, team_id=team.id, group_id="Fake", user_id=user_id, role=role)


def test_add_user_to_group_where_user_does_not_exists(repo, team_with_a_user_and_empty_team):
    team = team_with_a_user_and_empty_team
    group_id = team.groups[0].id
    user_id = "Fake"
    role = DCERoleEnum.User.name

    with pytest.raises(UserDoesNotExist):
        add_user_to_group(repo, team_id=team.id, group_id=group_id, user_id=user_id, role=role)


def test_add_user_to_group_where_user_already_in_group(repo, user_in_group):
    group_id = user_in_group.group_id
    team_id = user_in_group.team_id
    user_id = user_in_group.id
    role = DCERoleEnum.User.name

    with pytest.raises(UserAlreadyInGroup):
        add_user_to_group(repo, team_id=team_id, group_id=group_id, user_id=user_id, role=role)


def test_change_user_group_role(repo, user_in_group):
    new_role = DCERoleEnum.Power_User.name
    updated_at = user_in_group.updated_at
    group_user = change_user_group_role(repo, team_id=user_in_group.team_id,
                                        group_id=user_in_group.group_id, user_id=user_in_group.id, new_role=new_role)

    assert group_user.role == new_role
    assert updated_at < group_user.updated_at


def test_change_user_group_role_does_not_exists(repo, user_in_group):
    new_role = "Fake"
    with pytest.raises(RoleDoesNotExist):
        change_user_group_role(repo, team_id=user_in_group.team_id,
                               group_id=user_in_group.group_id, user_id=user_in_group.id, new_role=new_role)


def test_change_user_group_role_where_user_does_not_exist(repo, user_in_group):
    new_role = DCERoleEnum.Power_User.name
    group_id = "Fake"

    with pytest.raises(GroupUserDoesNotExist):
        change_user_group_role(repo, team_id=user_in_group.team_id,
                               group_id=group_id, user_id=user_in_group.id, new_role=new_role)


def test_list_group_users(repo, team_with_user_in_3_groups):
    team = team_with_user_in_3_groups
    group_users = list_group_users(repo, team.id, team.groups[0].id)

    assert len(group_users) == 2


def test_list_groups_of_user(repo, team_with_user_in_3_groups):
    team = team_with_user_in_3_groups
    groups = list_groups_of_user(repo, team.id, team.users[0].id)

    assert len(groups) == 3
