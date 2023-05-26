from uuid import UUID
import typer

from organization_auth.adapters.repositories.teams import TeamsDynamoDBRepository
from organization_auth.cli.view import show_group, show_groups
from organization_auth.service_layer import teams as service
from organization_auth.service_layer.exceptions import (
    GroupDoesNotExist, GroupUserDoesNotExist, RoleDoesNotExist, UserAlreadyInGroup, UserDoesNotExist
)


app = typer.Typer()
repo = TeamsDynamoDBRepository()


@app.command()
def get(team_id: UUID, group_id: UUID, user_id: UUID):
    """Gets a User in a Group of a Team"""
    group_user = service.get_user_in_group(team_id, group_id, user_id)
    show_group(group_user)


@app.command()
def add(team_id: UUID, group_id: UUID, user_id: UUID, role: str):
    """Adds a User to a Group of a Team with a given role"""
    try:
        group_user = service.add_user_to_group(team_id=team_id, group_id=group_id, user_id=user_id)
        show_group(group_user)
    except UserDoesNotExist:
        pass
    except GroupDoesNotExist:
        pass
    except UserAlreadyInGroup:
        pass


@app.command()
def rerole(team_id: UUID, group_id: UUID, user_id: UUID, new_role: str):
    """Changes the role of the User in the Group"""
    try:
        group_user = service.change_user_group_role(team_id=team_id,
                                                    group_id=group_id,
                                                    user_id=user_id,
                                                    new_role=new_role)
        show_group(group_user)
    except GroupUserDoesNotExist:
        pass
    except RoleDoesNotExist:
        pass


@app.command()
def ls(team_id: UUID, user_id: UUID):
    """List all Groups where a User belongs to"""
    user_groups = service.list_groups_of_user(team_id=team_id, user_id=user_id)
    show_groups(user_groups)
