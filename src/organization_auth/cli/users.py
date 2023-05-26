from uuid import UUID
import typer

from organization_auth.adapters.repositories.teams import TeamsDynamoDBRepository
from organization_auth.cli.view import show_group, show_groups
from organization_auth.service_layer import users as service
from organization_auth.service_layer.exceptions import RoleDoesNotExist, UserAlreadyExists


app = typer.Typer()
repo = TeamsDynamoDBRepository()


@app.command()
def new(team_id: UUID, user_id: UUID, name: str, role: str):
    """Creates a new User in a Team"""
    try:
        user = service.create_user(repo, team_id=team_id, user_id=user_id, name=name, role=role)
        show_group(user)
    except UserAlreadyExists:
        pass


@app.command()
def get(user_id: UUID):
    """Gets a User"""
    try:
        user = service.get_user(repo, user_id=user_id)
        show_group(user)
    except UserAlreadyExists:
        pass


@app.command()
def rm(user_id: UUID):
    """Marks a user as deleted. This action cannot be reversed"""
    if typer.confirm("You can undo this action. Are you sure you want to delete it?"):
        try:
            user = service.delete_user(repo, user_id=user_id)
            show_group(user)
        except UserAlreadyExists:
            pass


@app.command()
def disable(user_id: UUID):
    """Disables a User"""
    try:
        user = service.disable_user(repo, user_id=user_id)
        show_group(user)
    except UserAlreadyExists:
        pass


@app.command()
def enable(user_id: UUID):
    """Enables a User"""
    try:
        user = service.enable_user(repo, user_id=user_id)
        show_group(user)
    except UserAlreadyExists:
        pass


@app.command()
def rename(user_id: UUID, new_name: str):
    """Renames a User"""
    try:
        user = service.change_user_name(repo, user_id=user_id, new_name=new_name)
        show_group(user)
    except UserAlreadyExists:
        pass


@app.command()
def rerole(user_id: UUID, new_role: str):
    """Changes role name of a User"""
    try:
        user = service.change_user_role(repo, user_id=user_id, new_name=new_role)
        show_group(user)
    except UserAlreadyExists:
        pass
    except RoleDoesNotExist:
        pass


@app.command()
def ls(team_id: UUID):
    """Lists all Users in a Team"""
    users = service.list_users(team_id)
    show_groups(users)
