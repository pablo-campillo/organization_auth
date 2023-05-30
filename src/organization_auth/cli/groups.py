from typing import Optional, List
from uuid import UUID, uuid4
import typer

from organization_auth.cli.console import error_console
from organization_auth.adapters.repositories.teams import TeamsDynamoDBRepository
from organization_auth.cli.view import show_group, show_groups
from organization_auth.service_layer import groups as service
from organization_auth.service_layer.exceptions import (
    GroupAlreadyExistsException, GroupDoesNotExistException, RoleDoesNotExistException
)


app = typer.Typer(no_args_is_help=True)
repo = TeamsDynamoDBRepository()


@app.command()
def new(team_id: UUID, name: str, role: str, group_id: Optional[UUID] = None,
        roles: Optional[List[str]] = None):
    """Creates a new group in a team"""
    if group_id is None:
        group_id = uuid4()
    try:
        group = service.create_group(repo, team_id=team_id, group_id=group_id, name=name, role=role, roles=roles)
        show_group(group, title="New Group Created")
    except GroupAlreadyExistsException:
        error_console.print(f"Group {team_id} already exists!")
        raise typer.Exit(code=1)


@app.command()
def ls(team_id: UUID):
    """Lists all groups in a team"""
    groups = service.list_groups(repo, team_id=team_id)
    show_groups(groups, title="List of Groups")


@app.command()
def rm(group_id: UUID):
    """Marks a group as deleted. This action cannot be reversed!"""
    if typer.confirm("You can undo this action. Are you sure you want to delete it?"):
        try:
            group = service.delete_group(repo, group_id=group_id)
            show_group(group, title="Group Deleted")
        except GroupDoesNotExistException:
            error_console.print(f"Group {group_id} does not exist!")
            raise typer.Exit(code=1)


@app.command()
def disable(group_id: UUID):
    """Disables a group"""
    try:
        group = service.disable_group(repo, group_id=group_id)
        show_group(group, title="Group Disabled")
    except GroupDoesNotExistException:
        error_console.print(f"Group {group_id} does not exist!")
        raise typer.Exit(code=1)


@app.command()
def enable(group_id: UUID):
    """Enables a group"""
    try:
        group = service.enable_group(repo, group_id=group_id)
        show_group(group, title="Group Enabled")
    except GroupDoesNotExistException:
        error_console.print(f"Group {group_id} does not exist!")
        raise typer.Exit(code=1)


@app.command()
def rename(group_id: UUID, new_name: str):
    """Renames a group of a team"""
    try:
        group = service.change_group_name(repo, group_id=group_id, new_name=new_name)
        show_group(group, title="Group Renamed")
    except GroupDoesNotExistException:
        error_console.print(f"Group {group_id} does not exist!")
        raise typer.Exit(code=1)


@app.command()
def rerole(group_id: UUID, new_role: str):
    """Changes the role name of a group"""
    try:
        group = service.change_group_role(repo, group_id=group_id, new_role=new_role)
        show_group(group, title="Group with new Role")
    except GroupDoesNotExistException:
        error_console.print(f"Group {group_id} does not exist!")
        raise typer.Exit(code=1)
    except RoleDoesNotExistException:
        error_console.print(f"Role {new_role} not allowed for group {group_id}!")
        raise typer.Exit(code=1)


@app.command()
def get(group_id: UUID):
    """Gets a group"""
    try:
        group = service.get_group(repo, group_id=group_id)
        show_group(group, title="Group Returned")
    except GroupDoesNotExistException:
        error_console.print(f"Group {group_id} does not exist!")
        raise typer.Exit(code=1)


@app.command()
def add_role(group_id: UUID, new_role: str):
    """Gets a group"""
    try:
        group = service.add_role(repo, group_id=group_id, new_role_name=new_role)
        show_group(group, title="Role added to Group")
    except GroupDoesNotExistException:
        error_console.print(f"Group {group_id} does not exist!")
        raise typer.Exit(code=1)
