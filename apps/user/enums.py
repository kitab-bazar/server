import graphene

from config.permissions import UserPermissions


UserByTypePermissionEnum = graphene.Enum.from_enum(UserPermissions.Permission)
