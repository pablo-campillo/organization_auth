from datetime import timedelta
from typing import Optional
from uuid import UUID
from organization_auth.adapters.tokens import JoseJWTTokenProcessor
import typer

from organization_auth.cli.console import error_console
from organization_auth.adapters.repositories.teams import TeamsDynamoDBRepository
from organization_auth.cli.view import show_access_token, show_group, show_groups
from organization_auth.service_layer import users as service
from organization_auth.service_layer import tokens as token_service
from organization_auth.service_layer.exceptions import (
    TeamDoesNotExistException, UserAlreadyExistsException, UserDoesNotExistException
)


app = typer.Typer(no_args_is_help=True)
repo = TeamsDynamoDBRepository()
token_processor = JoseJWTTokenProcessor()


@app.command()
def new(team_id: UUID, user_id: UUID, name: str, role: str):
    """Creates a new User in a Team"""
    try:
        user = service.create_user(repo, team_id=team_id, user_id=user_id, name=name, role=role)
        show_group(user)
    except TeamDoesNotExistException:
        error_console.print(f"Team {team_id} does not exist!")
        raise typer.Exit(code=1)
    except UserAlreadyExistsException:
        error_console.print(f"User {user_id} already exists!")
        raise typer.Exit(code=1)


@app.command()
def get(user_id: UUID):
    """Gets a User"""
    try:
        user = service.get_user(repo, user_id=user_id)
        show_group(user)
    except UserDoesNotExistException:
        error_console.print(f"User {user_id} does not exists!")
        raise typer.Exit(code=1)


@app.command()
def rm(user_id: UUID):
    """Marks a user as deleted. This action cannot be reversed"""
    if typer.confirm("You can undo this action. Are you sure you want to delete it?"):
        try:
            user = service.delete_user(repo, user_id=user_id)
            show_group(user)
        except UserDoesNotExistException:
            error_console.print(f"User {user_id} does not exists!")
            raise typer.Exit(code=1)


@app.command()
def disable(user_id: UUID):
    """Disables a User"""
    try:
        user = service.disable_user(repo, user_id=user_id)
        show_group(user)
    except UserDoesNotExistException:
        error_console.print(f"User {user_id} does not exists!")
        raise typer.Exit(code=1)


@app.command()
def enable(user_id: UUID):
    """Enables a User"""
    try:
        user = service.enable_user(repo, user_id=user_id)
        show_group(user)
    except UserDoesNotExistException:
        error_console.print(f"User {user_id} does not exists!")
        raise typer.Exit(code=1)


@app.command()
def rename(user_id: UUID, new_name: str):
    """Renames a User"""
    try:
        user = service.change_user_name(repo, user_id=user_id, new_name=new_name)
        show_group(user)
    except UserDoesNotExistException:
        error_console.print(f"User {user_id} does not exists!")
        raise typer.Exit(code=1)


@app.command()
def rerole(user_id: UUID, new_role: str):
    """Changes role name of a User"""
    try:
        user = service.change_user_role(repo, user_id=user_id, new_name=new_role)
        show_group(user)
    except UserDoesNotExistException:
        error_console.print(f"User {user_id} does not exists!")
        raise typer.Exit(code=1)


@app.command()
def ls(team_id: UUID):
    """Lists all Users in a Team"""
    users = service.list_users(team_id)
    show_groups(users)


@app.command()
def access_token(user_id: UUID, exp: Optional[int] = None):
    """Creates an access token for a User."""

    expires_delta = timedelta(minutes=exp) if exp else None

    try:
        access_token = token_service.create_access_token(
            repo=repo,
            token_processor=token_processor,
            user_id=user_id, expires_delta=expires_delta)
    except UserDoesNotExistException:
        error_console.print(f"User {user_id} does not exists!")
        raise typer.Exit(code=1)

    user_token = token_service.decode_access_token(token_processor=token_processor, token=access_token)

    show_access_token(access_token, user_token)
