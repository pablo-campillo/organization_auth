from uuid import uuid4
from typing import List, Optional
from pydantic import UUID4
from organization_auth.adapters.repositories.teams import TeamsAbstractRepository

from organization_auth.domain.teams import Team
from organization_auth.service_layer.exceptions import TeamAlreadyExistsException, TeamDoesNotExistException


def create_team(repo: TeamsAbstractRepository, name: str, team_id: Optional[UUID4] = None) -> Team:
    if team_id is None:
        team_id = uuid4()
    elif (team := repo.get_team(team_id)) is not None:
        raise TeamAlreadyExistsException()
    team = Team(id=team_id, name=name)
    return repo.save_team(team)


def delete_team(repo: TeamsAbstractRepository, team_id: UUID4) -> Team:
    if (team := repo.get_team(team_id)) is not None:
        team.deleted = True
        return repo.save_team(team)
    else:
        raise TeamDoesNotExistException()


def disable_team(repo: TeamsAbstractRepository, team_id: UUID4) -> Team:
    if (team := repo.get_team(team_id)) is not None:
        team.enabled = False
        return repo.save_team(team)
    else:
        raise TeamDoesNotExistException()


def enable_team(repo: TeamsAbstractRepository, team_id: UUID4) -> Team:
    if (team := repo.get_team(team_id)) is not None:
        team.enabled = True
        return repo.save_team(team)
    else:
        raise TeamDoesNotExistException()


def change_team_name(repo: TeamsAbstractRepository, team_id: UUID4, new_name: str) -> Team:
    if (team := repo.get_team(team_id)) is not None:
        team.name = new_name
        return repo.save_team(team)
    else:
        raise TeamDoesNotExistException()


def get_team(repo: TeamsAbstractRepository, team_id: UUID4) -> Team:
    if (team := repo.get_team(team_id)) is not None:
        return team
    else:
        raise TeamDoesNotExistException()


def list_teams(repo: TeamsAbstractRepository) -> List[Team]:
    return repo.list_teams()
