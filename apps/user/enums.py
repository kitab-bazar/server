import graphene

from config.permissions import UserPermissions
from utils.graphene.enums import (
    convert_enum_to_graphene_enum,
    get_enum_name_from_django_field,
)

from .models import User


UserTypeEnum = convert_enum_to_graphene_enum(User.UserType, name='UserTypeEnum')

enum_map = {
    get_enum_name_from_django_field(field): enum
    for field, enum in (
        (User.user_type, UserTypeEnum),
    )
}

UserByTypePermissionEnum = graphene.Enum.from_enum(UserPermissions.Permission)
