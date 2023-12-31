from uuid import UUID
import typer

from organization_auth.cli.console import error_console
from organization_auth.adapters.repositories.teams import TeamsDynamoDBRepository
from organization_auth.cli.view import show_group_user, show_group_users
from organization_auth.service_layer import group_user as service
from organization_auth.service_layer.exceptions import (
    GroupDoesNotExistException, GroupUserDoesNotExistException, RoleDoesNotExistException,
    UserAlreadyInGroupException, UserDoesNotExistException
)


app = typer.Typer(no_args_is_help=True)
repo = TeamsDynamoDBRepository()


@app.command()
def get(team_id: UUID, group_id: UUID, user_id: UUID):
    """Gets a User in a Group of a Team"""
    try:
        group_user = service.get_user_in_group(team_id, group_id, user_id)
        show_group_user(group_user, title="Group User Returned")
    except UserDoesNotExistException:
        error_console.print(f"User {user_id} does not exist!")
        raise typer.Exit(code=1)


@app.command()
def add(group_id: UUID, user_id: UUID, role: str):
    """Adds a User to a Group of a Team with a given role"""
    try:
        group_user = service.add_user_to_group(repo, group_id=group_id, user_id=user_id, role=role)
        show_group_user(group_user, title="User added to Group")
    except UserDoesNotExistException:
        error_console.print(f"User {user_id} does not exist!")
        raise typer.Exit(code=1)
    except GroupDoesNotExistException:
        error_console.print(f"Group {group_id} does not exist!")
        raise typer.Exit(code=1)
    except UserAlreadyInGroupException:
        error_console.print(f"User {user_id} is already in Group {group_id}!")
        raise typer.Exit(code=1)


@app.command()
def rerole(team_id: UUID, group_id: UUID, user_id: UUID, new_role: str):
    """Changes the role of the User in the Group"""
    try:
        group_user = service.change_user_group_role(repo=repo,
                                                    team_id=team_id,
                                                    group_id=group_id,
                                                    user_id=user_id,
                                                    new_role=new_role)
        show_group_user(group_user, title="Group User with new Role")
    except GroupUserDoesNotExistException:
        error_console.print(f"Group {group_id} does not exist!")
        raise typer.Exit(code=1)
    except RoleDoesNotExistException:
        error_console.print(f"Role {new_role} not in Group {group_id}!")
        raise typer.Exit(code=1)


@app.command()
def ls(team_id: UUID, group_id: UUID):
    """List all Groups where a User belongs to"""
    user_groups = service.list_group_users(repo=repo, team_id=team_id, group_id=group_id)
    show_group_users(user_groups, title=f"List of Users of Group: {group_id}")
