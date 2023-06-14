

from pathlib import Path
from organization_auth.adapters.file_back import FileAbstractRepository
from organization_auth.adapters.repositories.teams import TeamsAbstractRepository
from organization_auth.service_layer.teams import list_all


def make_backup(repo: TeamsAbstractRepository,
                file_repo: FileAbstractRepository, file: Path):
    items = list_all(repo)
    file_repo.save_items(file, items)


def restore_backup(repo: TeamsAbstractRepository,
                   file_repo: FileAbstractRepository, file: Path):
    if not file.exists():
        raise FileExistsError()
    items = file_repo.load_items(file)
    repo.save_all(items)
