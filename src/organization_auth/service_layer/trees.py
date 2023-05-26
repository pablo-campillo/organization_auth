from typing import List
from pydantic import UUID4

from organization_auth.adapters.repositories.teams import TeamsAbstractRepository
from organization_auth.domain.teams import Team
from organization_auth.service_layer.group_user import list_group_users
from organization_auth.service_layer.groups import get_group, list_groups
from organization_auth.service_layer.teams import get_team
from organization_auth.service_layer.users import list_users


def tree_teams(repo: TeamsAbstractRepository) -> List[Team]:
    teams = repo.list_teams()
    for team in teams:
        team.users = list_users(repo, team.id)
        team.groups = list_groups(repo, team.id)
        for group in team.groups:
            group.users = list_group_users(repo, team_id=group.team_id, group_id=group.id)

    return teams


def tree_team(repo: TeamsAbstractRepository, team_id: UUID4) -> List[Team]:
    team = get_team(repo, team_id=team_id)

    team.users = list_users(repo, team.id)
    team.groups = list_groups(repo, team.id)
    for group in team.groups:
        group.users = list_group_users(repo, team_id=group.team_id, group_id=group.id)

    return team


def tree_group(repo: TeamsAbstractRepository, team_id: UUID4, group_id: UUID4) -> List[Team]:
    group = get_group(repo, group_id=group_id)

    group.users = list_group_users(repo, team_id=group.team_id, group_id=group.id)

    return group
