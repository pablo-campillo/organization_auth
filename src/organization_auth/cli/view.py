from typing import List
from rich.table import Table
from rich.tree import Tree

from organization_auth.cli.console import console
from organization_auth.domain.groups import Group
from organization_auth.domain.teams import Team
from organization_auth.domain.users import User


def show_team(team: Team):
    table = Table("Field", "Value")

    table.add_row("ID", str(team.id))
    table.add_row("Name", team.name)
    table.add_row("Enabled", str(team.enabled))
    table.add_row("Deleted", str(team.deleted))
    table.add_row("CreatedAt", team.created_at.isoformat())
    table.add_row("UpdatedAt", team.updated_at.isoformat())

    console.print(table)


def show_teams(teams: List[Team]):
    table = Table("ID", "Name", "Enabled", "Deleted", "CreatedAt", "DeletedAt")

    for team in teams:
        table.add_row(
            str(team.id),
            team.name,
            str(team.enabled),
            str(team.deleted),
            team.created_at.isoformat(),
            team.updated_at.isoformat(),
        )

    console.print(table)


def show_group(group: Group):
    table = Table("Field", "Value")

    table.add_row("ID", str(group.id))
    table.add_row("TeamID", str(group.team_id))
    table.add_row("Name", group.name)
    table.add_row("Enabled", str(group.enabled))
    table.add_row("Deleted", str(group.deleted))
    table.add_row("Roles", str(group.roles))
    table.add_row("CreatedAt", group.created_at.isoformat())
    table.add_row("UpdatedAt", group.updated_at.isoformat())

    console.print(table)


def show_group_user(group: Group):
    table = Table("Field", "Value")

    table.add_row("ID", str(group.id))
    table.add_row("TeamID", str(group.team_id))
    table.add_row("Role", str(group.role))
    table.add_row("CreatedAt", group.created_at.isoformat())
    table.add_row("UpdatedAt", group.updated_at.isoformat())

    console.print(table)


def show_groups(groups: List[Group]):
    table = Table("ID", "TeamID", "Name", "Enabled", "Deleted", "CreatedAt", "DeletedAt")    

    for group in groups:
        table.add_row(
            str(group.id),
            str(group.team_id),
            group.name,
            str(group.enabled),
            str(group.deleted),
            group.created_at.isoformat(),
            group.updated_at.isoformat(),
        )

    console.print(table)


def show_tree_teams(teams: List[Team]):
    tree = Tree("Organization")

    for team in teams:
        add_team_tree(tree, team)

    console.print(tree)


def show_tree_team(team: Team):
    tree = Tree("Organization")

    add_team_tree(tree, team)

    console.print(tree)


def add_team_tree(root: Tree, team: Team) -> Tree:
    team_tree = root.add(f"{team.name} ({team.id})")

    if team.users:
        add_users_subtree(team_tree, team.users)

    if team.groups:
        add_groups_subtree(team_tree, team.groups)

    return team_tree


def add_users_subtree(root: Tree, users: List[User]) -> Tree:
    users_tree = root.add("Users")
    for user in users:
        users_tree.add(f"{user.name} ({user.id})")
    return users_tree


def add_groups_subtree(root: Tree, groups: List[Group]) -> Tree:
    groups_tree = root.add("Groups")
    for group in groups:
        group_tree = groups_tree.add(f"{group.name} ({group.id}) - Roles: {(group.roles)} ({group.role})")
        for group_user in group.users:
            group_tree.add(f"User: {group_user.id} - {group_user.role}")

    return groups_tree
