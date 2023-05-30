from pathlib import Path
from organization_auth.service_layer.maintenance import make_backup, restore_backup
import typer

from organization_auth.cli.console import error_console
from organization_auth.adapters.file_back import FileRepository
from organization_auth.adapters.dynamodb.base import DDBOrganizationModel
from organization_auth.cli import teams
from organization_auth.cli import groups
from organization_auth.cli import users
from organization_auth.cli import group_users
from organization_auth.adapters.repositories.teams import TeamsDynamoDBRepository

app = typer.Typer(no_args_is_help=True)
repo = TeamsDynamoDBRepository()
file_repo = FileRepository()


app.add_typer(teams.app, name="teams", help="Manages teams")
app.add_typer(groups.app, name="groups", help="Manages groups in teams")
app.add_typer(users.app, name="users", help="Manages users in a team")
app.add_typer(group_users.app, name="group-users", help="Manages users in groups of a team")


@app.callback()
def callback():
    """
    CLI app for managing organization entities (Teams, Groups and Users).
    """


@app.command()
def back(file: str):
    make_backup(repo, file_repo, Path(file))


@app.command()
def restore(file: str):
    try:
        restore_backup(repo, file_repo, Path(file))
    except FileExistsError:
        error_console.print(f"File {file} not found!")


@app.command()
def db_init():
    """Creates Table in DynamoDB if it does not exist"""
    if not DDBOrganizationModel.exists():
        DDBOrganizationModel.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)


@app.command()
def db_clear():
    """Deletes Table in DynamoDB"""
    DDBOrganizationModel.delete_table()


if __name__ == "__main__":
    app()
