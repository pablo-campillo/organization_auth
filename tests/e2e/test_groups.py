from uuid import uuid4, UUID
import pytest

from organization_auth.domain.roles import DCERoleEnum
from organization_auth.service_layer.exceptions import GroupAlreadyExists, GroupDoesNotExist, RoleDoesNotExist
from organization_auth.service_layer.groups import change_group_name, change_group_role, create_group, delete_group, disable_group, enable_group, list_groups


def test_create_group(repo, empty_team):
    group_id = uuid4()
    name = "MyGroup"
    role = DCERoleEnum.User.name
    group = create_group(repo, team_id=empty_team.id, group_id=group_id, name=name, role=role)

    assert group.id == group_id
    assert group.team_id == empty_team.id
    assert group.name == name
    assert group.enabled
    assert not group.deleted


def test_create_group_with_auto_id(repo, empty_team):
    name = "MyGroup"
    role = DCERoleEnum.User.name
    group = create_group(repo, team_id=empty_team.id, name=name, role=role)

    assert isinstance(group.id, UUID)
    assert group.team_id == empty_team.id
    assert group.name == name
    assert group.enabled
    assert not group.deleted


def test_create_group_already_exists(repo, empty_group):
    role = DCERoleEnum.User.name
    name = "MyGroup"

    with pytest.raises(GroupAlreadyExists):
        create_group(repo, team_id=empty_group.team_id, group_id=empty_group.id, name=name, role=role)


def test_delete_group(repo, empty_group):
    team = delete_group(repo, group_id=empty_group.id)

    assert team.deleted


def test_delete_group_does_not_exists(repo):
    with pytest.raises(GroupDoesNotExist):
        delete_group(repo, group_id="Fake")


def test_disable_group(repo, empty_group):
    group = disable_group(repo, group_id=empty_group.id)

    assert not group.enabled


def test_diable_group_does_not_exists(repo):
    with pytest.raises(GroupDoesNotExist):
        disable_group(repo, group_id="Fake")


def test_enable_group(repo, empty_group):
    group = enable_group(repo, group_id=empty_group.id)

    assert group.enabled


def test_enable_group_does_not_exists(repo):
    with pytest.raises(GroupDoesNotExist):
        enable_group(repo, group_id="Fake")


def test_change_group_name(repo, empty_group):
    new_name = "MyNewGroupName"
    updated_at = empty_group.updated_at
    group = change_group_name(repo, group_id=empty_group.id, new_name=new_name)

    assert group.name == new_name
    assert updated_at < group.updated_at


def test_change_group_name_does_not_exists(repo):
    new_name = "MyNewgroupName"
    with pytest.raises(GroupDoesNotExist):
        change_group_name(repo, group_id="Fake", new_name=new_name)


def test_change_group_role(repo, empty_group):
    new_role = 'Team_Owner'
    updated_at = empty_group.updated_at
    group = change_group_role(repo, group_id=empty_group.id, new_role=new_role)

    assert group.role == new_role
    assert updated_at < group.updated_at


def test_change_group_role_does_not_exists(repo):
    new_role = 'Team_Owner'
    with pytest.raises(GroupDoesNotExist):
        change_group_role(repo, group_id="Fake", new_role=new_role)


def test_change_group_role_bad_role_name(repo, empty_group):
    new_role = 'Fake'
    with pytest.raises(RoleDoesNotExist):
        change_group_role(repo, group_id=empty_group.id, new_role=new_role)


def test_list_group(repo, team_with_5_groups):
    groups = list_groups(repo, team_id=team_with_5_groups.id)

    assert len(groups) == 5
