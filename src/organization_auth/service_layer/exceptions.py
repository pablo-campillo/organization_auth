class TeamAlreadyExists(Exception):
    pass


class TeamDoesNotExist(Exception):
    pass


class GroupAlreadyExists(Exception):
    pass


class GroupDoesNotExist(Exception):
    pass


class RoleDoesNotExist(Exception):
    pass


class UserAlreadyExists(Exception):
    pass


class UserDoesNotExist(Exception):
    pass


class UserAlreadyInGroup(Exception):
    pass


class GroupUserDoesNotExist(Exception):
    pass
