from datetime import datetime
from typing import List
from organization_auth.domain.base import DCEBaseModel
from organization_auth.domain.tokens import UserToken
from rich.table import Table
from rich.tree import Tree

from organization_auth.cli.console import console
from organization_auth.domain.groups import Group, GroupUser
from organization_auth.domain.teams import Team
from organization_auth.domain.users import User


def show_team(team: Team, title: str):
    table = Table("Field", "Value",
                  title=f":office_building: {title}", header_style="grey50")

    table.add_row("ID", str(team.id))
    table.add_row("Name", team.name)
    table.add_row("Enabled", _bool_value_icon(team.enabled))
    table.add_row("Deleted", _bool_value_icon(team.deleted))
    table.add_row("CreatedAt", _format_datetime(team.created_at))
    table.add_row("UpdatedAt", _format_datetime(team.updated_at))

    console.print(table)


def show_teams(teams: List[Team], title: str):
    table = Table("ID", "Name", "Enabled", "Deleted", "CreatedAt", "DeletedAt",
                  title=f":office_building: {title}", header_style="grey50")

    for team in teams:
        table.add_row(
            str(team.id),
            team.name,
            _bool_value_icon(team.enabled),
            _bool_value_icon(team.deleted),
            _format_datetime(team.created_at),
            _format_datetime(team.updated_at),
        )

    console.print(table)


def show_group(group: Group, title: str):
    table = Table("Field", "Value",
                  title=f":family: {title}", header_style="grey50")

    table.add_row("ID", str(group.id))
    table.add_row("TeamID", str(group.team_id))
    table.add_row("Name", group.name)
    table.add_row("Enabled", _bool_value_icon(group.enabled))
    table.add_row("Deleted", _bool_value_icon(group.deleted))
    table.add_row("Roles", str(group.roles))
    table.add_row("CreatedAt", _format_datetime(group.created_at))
    table.add_row("UpdatedAt", _format_datetime(group.updated_at))

    console.print(table)


def show_user(group: Group, title: str):
    table = Table("Field", "Value",
                  title=f":family: {title}", header_style="grey50")

    table.add_row("[grey50]ID", str(group.id))
    table.add_row("[grey50]TeamID", str(group.team_id))
    table.add_row("[grey50]Name", group.name)
    table.add_row("[grey50]Enabled", _bool_value_icon(group.enabled))
    table.add_row("[grey50]Deleted", _bool_value_icon(group.deleted))
    table.add_row("[grey50]CreatedAt", _format_datetime(group.created_at))
    table.add_row("[grey50]UpdatedAt",  _format_datetime(group.updated_at))

    console.print(table)


def show_users(users: List[User], title: str):
    table = Table("ID", "TeamID", "Name", "Enabled", "Deleted", "CreatedAt", "DeletedAt", 
                  title=f":adult: {title}", header_style="grey50")

    for user in users:
        table.add_row(
            str(user.id),
            str(user.team_id),
            user.name,
            _bool_value_icon(user.enabled),
            _bool_value_icon(user.deleted),
            _format_datetime(user.created_at),
            _format_datetime(user.updated_at),
        )

    console.print(table)


def show_group_user(group_user: GroupUser, title: str):
    table = Table("Field", "Value",
                  title=f":adult: {title}", header_style="grey50")

    table.add_row("ID", str(group_user.id))
    table.add_row("TeamID", str(group_user.team_id))
    table.add_row("GroupID", str(group_user.group_id))
    table.add_row("Role", str(group_user.role))
    table.add_row("CreatedAt", _format_datetime(group_user.created_at))
    table.add_row("UpdatedAt", _format_datetime(group_user.updated_at))

    console.print(table)


def show_group_users(group_users: List[GroupUser], title: str):
    table = Table("ID", "TeamID", "GroupID", "Role", "CreatedAt", "DeletedAt",
                  title=f":adult: {title}", header_style="grey50")

    for group_user in group_users:
        table.add_row(
            str(group_user.id),
            str(group_user.team_id),
            str(group_user.group_id),
            str(group_user.role),
            _format_datetime(group_user.created_at),
            _format_datetime(group_user.updated_at),
        )

    console.print(table)


def show_groups(groups: List[Group], title: str):
    table = Table("ID", "TeamID", "Name", "Enabled", "Deleted", "CreatedAt", "DeletedAt",
                  title=f":adult: {title}", header_style="grey50")

    for group in groups:
        table.add_row(
            str(group.id),
            str(group.team_id),
            group.name,
            _bool_value_icon(group.enabled),
            _bool_value_icon(group.deleted),
            _format_datetime(group.created_at),
            _format_datetime(group.updated_at),
        )

    console.print(table)


def show_access_token(access_token: str, user_token: UserToken):
    console.rule("[bright_magenta]Access Token", align="left")
    console.print(access_token)
    console.rule("[bright_magenta]Access Token Content", align="left")
    console.print(user_token.dict())


def show_tree_teams(teams: List[Team]):
    tree = Tree("[blue]Organization[/blue]")

    for team in teams:
        add_team_tree(tree, team)

    console.print(tree)


def show_tree_team(team: Team):
    tree = Tree("[blue]Organization[/blue]")

    add_team_tree(tree, team)

    console.print(tree)


def add_team_tree(root: Tree, team: Team) -> Tree:
    team_tree = root.add(f"+ :office_building: [underline blue][bold]{team.name}[/bold] ([grey50]{team.id}[/grey50])")

    if team.users:
        add_users_subtree(team_tree, team)

    if team.groups:
        add_groups_subtree(team_tree, team)

    return team_tree


def add_users_subtree(root: Tree, team: Team) -> Tree:
    users_tree = root.add("+ [purple]Users[/purple]")
    for user in team.users:
        users_tree.add(f":adult: [purple]{user.name}[/purple] ([grey50]{user.id}[/grey50])")
    return users_tree


def add_groups_subtree(root: Tree, team: Team) -> Tree:
    groups_tree = root.add("+ [green]Groups[/green]")
    for group in team.groups:
        group_tree = groups_tree.add(
            f"+ :family: [green]{group.name}[/green] ([grey50]{group.id}[/grey50]) - Roles: {_format_roles(group)}"
        )
        for group_user in group.users:
            group_tree.add(f":adult: [purple]{team.get_user(user_id=group_user.id).name}[/purple] "
                           f"[grey50]({group_user.id})[/grey50] - {group_user.role}")

    return groups_tree


def _format_roles(group: Group):
    result = "{"

    roles = [
        f"[grey50]{role}[/grey50]" if role != group.role else f"[white]{role}[/white]"
        for role in group.roles
    ]

    result += ", ".join(roles)
    result += "}"
    return result


def _bool_value_icon(value: bool) -> str:
    return ":white_heavy_check_mark:" if value else ":cross_mark:"


def _format_datetime(dt: datetime) -> str:
    return f"{dt.strftime('%Y-%m-%d')} [gray50]{dt.strftime('%H:%M:%S')} UTC"


def show_all(items: List[DCEBaseModel]):
    console.print(items)
