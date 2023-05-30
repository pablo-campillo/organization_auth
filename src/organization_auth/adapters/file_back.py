import abc
import json
from pathlib import Path
from typing import List
from organization_auth.domain.base import DCEBaseModel

from organization_auth.domain.groups import Group, GroupUser

from organization_auth.domain.teams import Team
from organization_auth.domain.users import User


class FileAbstractRepository(abc.ABC):

    @abc.abstractmethod
    def save_items(self, items: List[DCEBaseModel]):  # pragma: no cover
        pass

    @abc.abstractmethod
    def load_items(self, file_path: Path) -> List[DCEBaseModel]:  # pragma: no cover
        pass


class FileRepository(abc.ABC):

    def save_items(self, file_path: Path, items: List[DCEBaseModel]):  # pragma: no cover
        with file_path.open('w') as f:
            for item in items:
                data = json.loads(item.json())
                data['cls'] = type(item).__name__
                f.write(json.dumps(data)+"\n")

    def load_items(self, file_path: Path) -> List[DCEBaseModel]:  # pragma: no cover
        result = []
        with file_path.open('r') as f:
            for item_data in f.readlines():
                data = json.loads(item_data)
                if data['cls'] == "Team":
                    del data['cls']
                    result.append(Team(**data))
                elif data['cls'] == "User":
                    del data['cls']
                    result.append(User(**data))
                elif data['cls'] == "Group":
                    del data['cls']
                    result.append(Group(**data))
                elif data['cls'] == "GroupUser":
                    del data['cls']
                    result.append(GroupUser(**data))
        return result
