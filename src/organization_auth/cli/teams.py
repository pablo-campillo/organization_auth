from typing import Optional
from uuid import UUID
import typer

from organization_auth.adapters.repositories.teams import TeamsDynamoDBRepository
from organization_auth.cli.console import console
from organization_auth.cli.input import warning_confirm
from organization_auth.cli.view import show_team, show_teams, show_tree_team, show_tree_teams
from organization_auth.service_layer import teams as teams_service
from organization_auth.service_layer import trees as trees_service

app = typer.Typer(no_args_is_help=True)
repo = TeamsDynamoDBRepository()


@app.command()
def new(name: str, team_id: Optional[UUID] = None):
    """Creates a new team"""
    team = teams_service.create_team(repo, name, team_id=team_id)
    show_team(team)


@app.command()
def ls():
    """Lists all teams in the organization"""
    teams = teams_service.list_teams(repo)
    show_teams(teams)


@app.command()
def rm(team_id: UUID):
    """Marks a team as deleted. It cannot be reversed!"""
    if warning_confirm("You can undo this action. Are you sure you want to delete it?"):
        team = teams_service.delete_team(repo, team_id)
        show_team(team)


@app.command()
def disable(team_id: UUID):
    """Disables a team"""
    team = teams_service.disable_team(repo, team_id)
    show_team(team)


@app.command()
def enable(team_id: UUID):
    """Enables a team"""
    team = teams_service.enable_team(repo, team_id)
    show_team(team)


@app.command()
def rename(team_id: UUID, new_name: str):
    """Renames a team"""
    team = teams_service.change_team_name(repo, team_id, new_name=new_name)
    show_team(team)


@app.command()
def get(team_id: UUID):
    """Gets a team"""
    team = teams_service.get_team(repo, team_id)
    show_team(team)


@app.command()
def tree(team_id: Optional[UUID] = None):
    """List all teams of the organization or just one given its id"""
    if team_id is None:
        with console.status("Working..."):
            teams = trees_service.tree_teams(repo)
        show_tree_teams(teams)
    else:
        with console.status("Working..."):
            team = trees_service.tree_team(repo, team_id=team_id)
        show_tree_team(team)


if __name__ == "__main__":
    app()
