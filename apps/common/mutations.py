import graphene
from utils.graphene.mutation import (
    generate_input_type_for_serializer,
    CreateUpdateGrapheneMutation,
    DeleteMutation
)

from apps.user.models import User
from apps.common.models import ActivityLogFile
from apps.common.schema import ActivityLogFileType
from apps.common.serializers import ActivityLogFileSerializer
from config.permissions import UserPermissions


ActivityLogFileInputType = generate_input_type_for_serializer(
    'ActivityLogFileInputType',
    serializer_class=ActivityLogFileSerializer
)


class BaseActivityLogFileMutationMixin():
    @classmethod
    def filter_queryset(cls, qs, info):
        if info.context.user.user_type == User.UserType.MODERATOR.value:
            return qs
        return qs.none()


class CreateActivityLogFile(BaseActivityLogFileMutationMixin, CreateUpdateGrapheneMutation):
    class Arguments:
        data = ActivityLogFileInputType(required=True)
    model = ActivityLogFile
    serializer_class = ActivityLogFileSerializer
    result = graphene.Field(ActivityLogFileType)
    permissions = [UserPermissions.Permission.ACTIVITY_LOG_FILE]


class DeleteActivityLogFile(BaseActivityLogFileMutationMixin, DeleteMutation):
    class Arguments:
        id = graphene.ID(required=True)
    model = ActivityLogFile
    result = graphene.Field(ActivityLogFileType)
    permissions = [UserPermissions.Permission.ACTIVITY_LOG_FILE]


class Mutation(graphene.ObjectType):
    create_activity_log_file = CreateActivityLogFile.Field()
    delete_activity_log_file = DeleteActivityLogFile.Field()
