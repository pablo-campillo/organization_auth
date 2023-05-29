from uuid import uuid4
from organization_auth.adapters.tokens import JoseJWTTokenProcessor
import pytest

from organization_auth.adapters.dynamodb.base import DDBOrganizationModel
from organization_auth.adapters.repositories.teams import TeamsDynamoDBRepository
from organization_auth.domain.groups import GroupUser
from organization_auth.service_layer.group_user import add_user_to_group
from organization_auth.service_layer.groups import create_group
from organization_auth.service_layer.teams import create_team
from organization_auth.service_layer.users import create_user


@pytest.fixture(autouse=True)
def reset_dynamodb_table():
    if DDBOrganizationModel.exists():
        DDBOrganizationModel.delete_table()
    DDBOrganizationModel.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)


@pytest.fixture()
def repo():
    return TeamsDynamoDBRepository()


@pytest.fixture()
def token_processor():
    return JoseJWTTokenProcessor()


@pytest.fixture()
def empty_team(repo):
    team_id = uuid4()
    name = 'MyTeam'
    return create_team(repo, team_id=team_id, name=name)


@pytest.fixture()
def database_5_empty_teams(repo):
    return [
        create_team(repo, team_id=uuid4(), name=f"MyTeam{i}")
        for i in range(5)
    ]


@pytest.fixture()
def empty_group(repo, empty_team):
    group_id = uuid4()
    name = "MyGroup"
    role = "User"
    return create_group(repo, team_id=empty_team.id, group_id=group_id, name=name, role=role, roles=["Team_Owner"])


@pytest.fixture()
def team_with_5_groups(repo, empty_team):
    name = "MyGroup"
    role = "User"
    empty_team.groups = [
        create_group(repo, team_id=empty_team.id, group_id=uuid4(), name=name+str(i), role=role)
        for i in range(5)
    ]
    return empty_team


@pytest.fixture()
def empty_user(repo, empty_team):
    user_id = uuid4()
    name = "MyUser"
    role = "User"
    return create_user(repo, team_id=empty_team.id, user_id=user_id, name=name, role=role)


@pytest.fixture()
def team_with_5_users(repo, empty_team):
    name = "MyUser"
    role = "User"
    empty_team.users = [
        create_user(repo, team_id=empty_team.id, user_id=uuid4(), name=name+str(i), role=role)
        for i in range(5)
    ]
    return empty_team


@pytest.fixture()
def team_with_a_user_and_empty_group(repo, empty_team):
    empty_team.users = [
        create_user(repo, team_id=empty_team.id, user_id=uuid4(), name="MyUser", role="User")
    ]
    empty_team.groups = [
        create_group(repo, team_id=empty_team.id, group_id=uuid4(), name="MyGroup", role="User",
                     roles=["User", "Power_User"])
    ]
    return empty_team


@pytest.fixture()
def user_in_group(repo, team_with_a_user_and_empty_group) -> GroupUser:
    team = team_with_a_user_and_empty_group
    group_id = team.groups[0].id
    user_id = team.users[0].id
    role = "User"
    return add_user_to_group(repo, group_id=group_id, user_id=user_id, role=role)


@pytest.fixture()
def team_with_user_in_3_groups(repo, empty_team):
    user_id1 = uuid4()
    user_id2 = uuid4()
    role = "User"
    roles = ["User", "Power_User", "Team_Owner"]
    empty_team.users = [
        create_user(repo, team_id=empty_team.id, user_id=user_id1, name="MyUser", role=role),
        create_user(repo, team_id=empty_team.id, user_id=user_id2, name="MyUser", role=role)
    ]
    empty_team.groups = [
        create_group(repo, team_id=empty_team.id, group_id=uuid4(), name="MyGroup0", role=role, roles=roles),
        create_group(repo, team_id=empty_team.id, group_id=uuid4(), name="MyGroup1", role=role, roles=roles),
        create_group(repo, team_id=empty_team.id, group_id=uuid4(), name="MyGroup2", role=role, roles=roles),
        create_group(repo, team_id=empty_team.id, group_id=uuid4(), name="MyGroup3", role=role, roles=roles),
        create_group(repo, team_id=empty_team.id, group_id=uuid4(), name="MyGroup4", role=role, roles=roles),
    ]
    empty_team.groups[0].users = [
        add_user_to_group(repo, group_id=empty_team.groups[0].id, user_id=user_id1, role="User"),
        add_user_to_group(repo, group_id=empty_team.groups[0].id, user_id=user_id2, role="User"),
    ]
    empty_team.groups[2].users = [
        add_user_to_group(repo, group_id=empty_team.groups[2].id, user_id=user_id1, role="Power_User"),
    ]

    empty_team.groups[4].users = [
        add_user_to_group(repo, group_id=empty_team.groups[4].id, user_id=user_id1, role="Team_Owner")
    ]
    return empty_team
