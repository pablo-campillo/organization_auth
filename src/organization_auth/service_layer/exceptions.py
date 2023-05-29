class TeamAlreadyExistsException(Exception):
    pass


class TeamDoesNotExistException(Exception):
    pass


class GroupAlreadyExistsException(Exception):
    pass


class GroupDoesNotExistException(Exception):
    pass


class RoleDoesNotExistException(Exception):
    pass


class UserAlreadyExistsException(Exception):
    pass


class UserDoesNotExistException(Exception):
    pass


class UserAlreadyInGroupException(Exception):
    pass


class GroupUserDoesNotExistException(Exception):
    pass


class TokenExpiredException(Exception):
    pass
