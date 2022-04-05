from utils.graphene.enums import (
    convert_enum_to_graphene_enum,
    get_enum_name_from_django_field,
)

from apps.package.models import (
    PublisherPackage,
    SchoolPackage,
    CourierPackage,
    InstitutionPackage,
)


PublisherPackageStatusEnum = convert_enum_to_graphene_enum(PublisherPackage.Status, name='PublisherPackageStatusEnum')
SchoolPackageStatusEnum = convert_enum_to_graphene_enum(SchoolPackage.Status, name='SchoolPackageStatusEnum')
CourierPackageStatusEnum = convert_enum_to_graphene_enum(CourierPackage.Status, name='CourierPackageStatusEnum')
InstitutionPackageStatusEnum = convert_enum_to_graphene_enum(InstitutionPackage.Status, name='InstitutionPackageStatusEnum')
CourierPackageTypeEnum = convert_enum_to_graphene_enum(CourierPackage.Type, name='CourierPackageTypeEnum')

enum_map = {
    get_enum_name_from_django_field(field): enum
    for field, enum in (
        (PublisherPackage.status, PublisherPackageStatusEnum),
        (SchoolPackage.status, SchoolPackageStatusEnum),
        (CourierPackage.status, CourierPackageStatusEnum),
        (InstitutionPackage.status, InstitutionPackageStatusEnum),
        (CourierPackage.type, CourierPackageTypeEnum),
    )
}
