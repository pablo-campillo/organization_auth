import uuid

from organization_auth.domain.teams import Team
from organization_auth.domain.users import User


def test_get_user():
    user_id = uuid.UUID("9bae91ad-791c-45ad-aa5d-65171398ebe5")
    team = Team(name="MyTeam")
    team.users.append(User(id=user_id, team_id=team.id, name="MyUser", role="User"))

    user = team.get_user(user_id=user_id)

    assert user


def test_get_user_not_found():
    user_id = uuid.UUID("9bae91ad-791c-45ad-aa5d-65171398ebe5")
    team = Team(name="MyTeam")
    team.users.append(User(id=user_id, team_id=team.id, name="MyUser", role="User"))

    user = team.get_user(user_id="Fake")

    assert not user
