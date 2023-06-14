from organization_auth.service_layer.exceptions import TokenExpiredException, UserDoesNotExistException
import pytest
from datetime import timedelta

from organization_auth.domain.utils import my_utc_now
from organization_auth.service_layer.tokens import create_access_token, decode_access_token


def test_create_access_token(repo, token_processor, team_with_user_in_3_groups):
    team = team_with_user_in_3_groups
    user_id = team.users[0].id

    access_token = create_access_token(repo, token_processor, user_id)

    data = decode_access_token(token_processor, access_token)

    assert my_utc_now() < data.exp
    assert team.id == data.team_id
    assert team.users[0].id == data.user_id
    assert len(data.groups) == 3


def test_create_access_token_with_custom_expiration(repo, token_processor, team_with_user_in_3_groups):
    team = team_with_user_in_3_groups
    user_id = team.users[0].id

    access_token = create_access_token(repo, token_processor, user_id, expires_delta=timedelta(minutes=30))

    data = decode_access_token(token_processor, access_token)

    assert (my_utc_now() + timedelta(minutes=29)) < data.exp


def test_create_access_token_user_does_not_exist(repo, token_processor):
    user_id = "Fake"

    with pytest.raises(UserDoesNotExistException):
        create_access_token(repo, token_processor, user_id, expires_delta=timedelta(minutes=30))


def test_decode_access_token_expired(repo, token_processor, team_with_user_in_3_groups):
    team = team_with_user_in_3_groups
    user_id = team.users[0].id

    access_token = create_access_token(repo, token_processor, user_id, expires_delta=-timedelta(minutes=30))

    with pytest.raises(TokenExpiredException):
        decode_access_token(token_processor, access_token)
