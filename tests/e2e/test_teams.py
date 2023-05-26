import pytest
from uuid import UUID, uuid4
from organization_auth.adapters.repositories.teams import TeamsDynamoDBRepository


from organization_auth.service_layer.exceptions import TeamAlreadyExists, TeamDoesNotExist
from organization_auth.service_layer.teams import (
    change_team_name, create_team, delete_team, disable_team, enable_team, get_team, list_teams
)


def test_create_team():
    repo = TeamsDynamoDBRepository()

    team_id = uuid4()
    name = 'MyTeam'
    team = create_team(repo, team_id=team_id, name=name)

    assert team.id == team_id
    assert team.name == name
    assert team.enabled
    assert not team.deleted


def test_create_team_auto_id():
    repo = TeamsDynamoDBRepository()

    name = 'MyTeam'
    team = create_team(repo, name=name)

    assert isinstance(team.id, UUID)
    assert team.name == name
    assert team.enabled
    assert not team.deleted


def test_create_team_already_exists_exception(repo, empty_team):
    with pytest.raises(TeamAlreadyExists):
        create_team(repo, team_id=empty_team.id, name="MyTeam")


def test_delete_team(repo, empty_team):
    team = delete_team(repo, team_id=empty_team.id)

    assert team.deleted


def test_delete_team_does_not_exists(repo):
    repo = TeamsDynamoDBRepository()

    with pytest.raises(TeamDoesNotExist):
        delete_team(repo, team_id="Fake")


def test_disable_team(repo, empty_team):
    team = disable_team(repo, team_id=empty_team.id)

    assert not team.enabled


def test_diable_team_does_not_exists(repo):
    with pytest.raises(TeamDoesNotExist):
        disable_team(repo, team_id="Fake")


def test_enable_team(repo, empty_team):
    team = enable_team(repo, team_id=empty_team.id)

    assert team.enabled


def test_enable_team_does_not_exists(repo):
    with pytest.raises(TeamDoesNotExist):
        enable_team(repo, team_id="Fake")


def test_change_team_name(repo, empty_team):
    new_name = "MyNewTeamName"
    updated_at = empty_team.updated_at
    team = change_team_name(repo, empty_team.id, new_name=new_name)

    assert team.name == new_name
    assert updated_at < team.updated_at


def test_change_team_name_does_not_exists(repo):
    new_name = "MyNewTeamName"
    with pytest.raises(TeamDoesNotExist):
        change_team_name(repo, team_id="Fake", new_name=new_name)


def test_get_team(repo, empty_team):
    team = get_team(repo, empty_team.id)

    assert team.id == empty_team.id
    assert team.name == empty_team.name


def test_get_team_does_not_exists(repo):
    with pytest.raises(TeamDoesNotExist):
        get_team(repo, team_id="Fake")


def test_list_teams(repo, database_5_empty_teams):
    teams = list_teams(repo)

    assert len(teams) == 5
