import graphene

from django.contrib.auth import login, logout

from utils.graphene.mutation import generate_input_type_for_serializer, CreateUpdateGrapheneMutation
from utils.graphene.error_types import CustomErrorType, mutation_is_not_valid
from config.permissions import UserPermissions

from apps.user.schema import UserType, UserMeType
from apps.user.serializers import (
    LoginSerializer,
    RegisterSerializer,
    ActivateSerializer,
    UserPasswordSerializer,
    GenerateResetPasswordTokenSerializer,
    ResetPasswordSerializer,
    UpdateProfileSerializer,
)
from .models import User


RegisterInputType = generate_input_type_for_serializer(
    'RegisterInputType',
    RegisterSerializer
)


class Register(graphene.Mutation):
    class Arguments:
        data = RegisterInputType(required=True)

    errors = graphene.List(graphene.NonNull(CustomErrorType))
    ok = graphene.Boolean()
    result = graphene.Field(UserType)

    @staticmethod
    def mutate(root, info, data):
        serializer = RegisterSerializer(
            data=data,
            context={'request': info.context.request}
        )
        if errors := mutation_is_not_valid(serializer):
            return Register(errors=errors, ok=False)
        instance = serializer.save()
        return Register(
            result=instance,
            errors=None,
            ok=True
        )


LoginInputType = generate_input_type_for_serializer(
    'LoginInputType',
    LoginSerializer
)


class Login(graphene.Mutation):
    class Arguments:
        data = LoginInputType(required=True)

    result = graphene.Field(UserMeType)
    errors = graphene.List(graphene.NonNull(CustomErrorType))
    ok = graphene.Boolean(required=True)

    @staticmethod
    def mutate(root, info, data):
        serializer = LoginSerializer(
            data=data,
            context={'request': info.context.request}
        )
        errors = mutation_is_not_valid(serializer)
        if errors:
            return Login(
                errors=errors,
                ok=False,
            )
        if user := serializer.validated_data.get('user'):
            login(info.context.request, user)
        return Login(
            result=user,
            errors=None,
            ok=True
        )


ActivateInputType = generate_input_type_for_serializer(
    'ActivateInputType',
    ActivateSerializer
)


class Activate(graphene.Mutation):
    class Arguments:
        data = ActivateInputType(required=True)

    errors = graphene.List(graphene.NonNull(CustomErrorType))
    ok = graphene.Boolean()

    @staticmethod
    def mutate(root, info, data):
        serializer = ActivateSerializer(
            data=data,
            context={'request': info.context.request}
        )
        errors = mutation_is_not_valid(serializer)
        if errors:
            return Activate(errors=errors, ok=False)
        return Activate(errors=None, ok=True)


class VerifyUser(CreateUpdateGrapheneMutation):
    class Arguments:
        id = graphene.ID(required=True)

    result = graphene.Field(UserType)
    ok = graphene.Boolean()
    permissions = [UserPermissions.Permission.CAN_VERIFY_USER]

    @classmethod
    def mutate(cls, root, info, id):
        user = User.objects.get(pk=id)
        user.is_verified = True
        user.verified_by = info.context.request.user
        user.save()
        return VerifyUser(result=user, ok=True)


ChangePasswordInputType = generate_input_type_for_serializer(
    'ChangePasswordInputType',
    UserPasswordSerializer
)


class ChangeUserPassword(graphene.Mutation):
    class Arguments:
        data = ChangePasswordInputType(required=True)

    errors = graphene.List(graphene.NonNull(CustomErrorType))
    ok = graphene.Boolean()
    result = graphene.Field(UserType)

    @staticmethod
    def mutate(root, info, data):
        serializer = UserPasswordSerializer(
            instance=info.context.user,
            data=data,
            context={'request': info.context.request},
            partial=True
        )
        if errors := mutation_is_not_valid(serializer):
            return ChangeUserPassword(errors=errors, ok=False)
        serializer.save()
        return ChangeUserPassword(result=info.context.user, errors=None, ok=True)


GenerateResetPasswordTokenType = generate_input_type_for_serializer(
    'GenerateResetPasswordTokenType',
    GenerateResetPasswordTokenSerializer
)


class GenerateResetPasswordToken(graphene.Mutation):
    class Arguments:
        data = GenerateResetPasswordTokenType(required=True)

    errors = graphene.List(graphene.NonNull(CustomErrorType))
    ok = graphene.Boolean()

    @staticmethod
    def mutate(root, info, data):
        serializer = GenerateResetPasswordTokenSerializer(data=data)
        if errors := mutation_is_not_valid(serializer):
            return GenerateResetPasswordToken(errors=errors, ok=False)
        return GenerateResetPasswordToken(errors=None, ok=True)


ResetPasswordType = generate_input_type_for_serializer(
    'ResetPasswordType',
    ResetPasswordSerializer
)


class ResetPassword(graphene.Mutation):
    class Arguments:
        data = ResetPasswordType(required=True)

    errors = graphene.List(graphene.NonNull(CustomErrorType))
    ok = graphene.Boolean()

    @staticmethod
    def mutate(root, info, data):
        serializer = ResetPasswordSerializer(data=data)
        if errors := mutation_is_not_valid(serializer):
            return ResetPassword(errors=errors, ok=False)
        return ResetPassword(errors=None, ok=True)


class Logout(graphene.Mutation):
    ok = graphene.Boolean()

    def mutate(self, info, *args, **kwargs):
        if info.context.user.is_authenticated:
            logout(info.context.request)
        return Logout(ok=True)


UpdateProfileType = generate_input_type_for_serializer(
    'UpdateProfileType',
    UpdateProfileSerializer
)


class UpdateProfile(graphene.Mutation):
    class Arguments:
        data = UpdateProfileType(required=True)

    errors = graphene.List(graphene.NonNull(CustomErrorType))
    ok = graphene.Boolean()
    result = graphene.Field(UserMeType)

    @staticmethod
    def mutate(root, info, data):
        serializer = UpdateProfileSerializer(
            instance=info.context.user,
            data=data,
            context={'request': info.context.request},
            partial=True,
        )
        if errors := mutation_is_not_valid(serializer):
            return UpdateProfile(errors=errors, ok=False)
        instance = serializer.save()
        return UpdateProfile(
            result=instance,
            errors=None,
            ok=True
        )


class Mutation(graphene.ObjectType):
    register = Register.Field()
    login = Login.Field()
    activate = Activate.Field()
    verify = VerifyUser.Field()
    logout = Logout.Field()
    change_password = ChangeUserPassword.Field()
    generate_reset_password_token = GenerateResetPasswordToken.Field()
    reset_password = ResetPassword.Field()
    update_profile = UpdateProfile.Field()
