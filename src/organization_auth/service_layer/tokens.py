from datetime import timedelta
from typing import Union
from uuid import UUID
from organization_auth.adapters.repositories.teams import TeamsAbstractRepository

from organization_auth.adapters.tokens import AbstractTokenProcessor
from organization_auth.domain.tokens import UserToken
from organization_auth.domain.utils import my_utc_now
from organization_auth.service_layer.exceptions import TokenExpiredException, UserDoesNotExistException
from organization_auth.service_layer.group_user import list_groups_of_user


def create_access_token(repo: TeamsAbstractRepository,
                        token_processor: AbstractTokenProcessor,
                        user_id: UUID, expires_delta: Union[timedelta, None] = None):
    if expires_delta:
        expire = my_utc_now() + expires_delta
    else:
        expire = my_utc_now() + timedelta(minutes=15)

    if (user := repo.get_user(user_id=user_id)) is not None:
        to_encode = {
            "exp": expire,
            "team_id": str(user.team_id),
            "user_id": str(user_id),
            "groups": [
                {"group_id": str(group.id), "role": group.role}
                for group in list_groups_of_user(repo, user.team_id, user_id)
            ]
        }
        access_token = token_processor.encode_token(to_encode)

        return access_token
    else:
        raise UserDoesNotExistException()


def decode_access_token(token_processor: AbstractTokenProcessor, token: str) -> UserToken:

    data = token_processor.decode_token(token)

    if data is None:
        raise TokenExpiredException()

    user_token = UserToken(**data)

    return user_token
