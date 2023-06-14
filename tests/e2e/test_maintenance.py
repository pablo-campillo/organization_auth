from pathlib import Path
from organization_auth.service_layer.trees import tree_teams
import pytest

from organization_auth.service_layer.maintenance import make_backup, restore_backup


def test_make_backup(repo, file_repo, team_with_user_in_3_groups, backup_file):
    make_backup(repo, file_repo, backup_file)

    with backup_file.open('r') as f:
        lines = f.readlines()

    assert len(lines) == 12


def test_restore_backup(repo, file_repo, team_with_user_in_3_groups, backup_file):
    make_backup(repo, file_repo, backup_file)

    restore_backup(repo, file_repo, backup_file)

    teams = tree_teams(repo)

    assert len(teams) == 1
    assert len(teams[0].users) == 2
    assert len(teams[0].groups) == 5


def test_restore_backup_file_does_not_exist(repo, file_repo, team_with_user_in_3_groups):
    with pytest.raises(FileExistsError):
        restore_backup(repo, file_repo, Path("Fake"))
