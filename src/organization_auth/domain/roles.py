# from enum import Enum, EnumMeta


# class MetaEnum(EnumMeta):
#     def __contains__(cls, item):
#         try:
#             cls(item)
#         except ValueError:
#             return False
#         return True


# class DCERoleEnum(str, Enum, metaclass=MetaEnum):
#     Team_Owner = "Team_Owner"
#     Power_User = "Power_User"
#     User = "User"

#     @classmethod
#     def is_valid(cls, role_name):
#         return role_name in cls


DCERoleEnum = str
