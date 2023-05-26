from organization_auth.service_layer.trees import tree_group, tree_team, tree_teams


def test_tree_teams(repo, team_with_user_in_3_groups):
    team = team_with_user_in_3_groups
    teams = tree_teams(repo)

    assert len(teams) == 1
    assert len(teams[0].users) == len(team.users)
    assert len(teams[0].groups) == len(team.groups)

    users_per_group = {
        group.id: len(group.users)
        for group in team.groups
    }

    for group in teams[0].groups:
        assert len(group.users) == users_per_group[group.id]


def test_tree_team(repo, team_with_user_in_3_groups):
    team = team_with_user_in_3_groups
    r_team = tree_team(repo, team.id)

    assert len(r_team.users) == len(team.users)
    assert len(r_team.groups) == len(team.groups)

    users_per_group = {
        group.id: len(group.users)
        for group in team.groups
    }

    for group in r_team.groups:
        assert len(group.users) == users_per_group[group.id]


def test_tree_group(repo, team_with_user_in_3_groups):
    team = team_with_user_in_3_groups
    r_group = tree_group(repo, team_id=team.id, group_id=team.groups[0].id)

    assert len(r_group.users) == len(team.groups[0].users)
