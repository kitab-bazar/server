import graphene
from apps.user.models import User
from utils.graphene.mutation import (
    generate_input_type_for_serializer,
    CreateUpdateGrapheneMutation,
)
from apps.package.serializers import (
    SchoolPackageUpdateSerializer,
    PublisherPackageUpdateSerializer,
    CourierPackageUpdateSerializer
)
from apps.package.models import (
    PublisherPackage,
    SchoolPackage,
    CourierPackage,
)
from apps.package.schema import (
    SchoolPackageType,
    PublisherPackageType,
    CourierPackageType
)


class packageMixin():
    @classmethod
    def filter_queryset(cls, qs, info):
        if info.context.user.user_type == User.UserType.MODERATOR.value:
            return qs
        return qs.none()

    @classmethod
    def check_permissions(cls, *args, **_):
        return True


SchoolPackageUpdateInputType = generate_input_type_for_serializer(
    'SchoolPackageUpdateInputType',
    serializer_class=SchoolPackageUpdateSerializer
)


class UpdateSchoolPackage(packageMixin, CreateUpdateGrapheneMutation):
    class Arguments:
        data = SchoolPackageUpdateInputType(required=True)
        id = graphene.ID(required=True)
    model = SchoolPackage
    serializer_class = SchoolPackageUpdateSerializer
    result = graphene.Field(SchoolPackageType)


PublisherPackageUpdateInputType = generate_input_type_for_serializer(
    'PublisherPackageUpdateInputType',
    serializer_class=PublisherPackageUpdateSerializer
)


class UpdatePublisherPackage(packageMixin, CreateUpdateGrapheneMutation):
    class Arguments:
        data = PublisherPackageUpdateInputType(required=True)
        id = graphene.ID(required=True)
    model = PublisherPackage
    serializer_class = PublisherPackageUpdateSerializer
    result = graphene.Field(PublisherPackageType)


CourierPackageUpdateInputType = generate_input_type_for_serializer(
    'CourierPackageUpdateInputType',
    serializer_class=CourierPackageUpdateSerializer
)


class UpdateCourierPackage(packageMixin, CreateUpdateGrapheneMutation):
    class Arguments:
        data = CourierPackageUpdateInputType(required=True)
        id = graphene.ID(required=True)
    model = CourierPackage
    serializer_class = CourierPackageUpdateSerializer
    result = graphene.Field(CourierPackageType)


class Mutation(graphene.ObjectType):
    update_school_package = UpdateSchoolPackage.Field()
    update_publisher_package = UpdatePublisherPackage.Field()
    update_courier_package = UpdateCourierPackage.Field()
