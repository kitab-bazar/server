import graphene

from config.permissions import (
    SchoolPermissions,
    InstitutionPermissions,
    PublisherPermissions,
    BookPermissions,
)


SchoolPermissionEnum = graphene.Enum.from_enum(SchoolPermissions.Permission)
InstitutionPermissionEnum = graphene.Enum.from_enum(InstitutionPermissions.Permission)
PublisherPermissionEnum = graphene.Enum.from_enum(PublisherPermissions.Permission)
BookPermissionEnum = graphene.Enum.from_enum(BookPermissions.Permission)
