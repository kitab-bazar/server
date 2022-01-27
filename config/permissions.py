from enum import Enum, auto, unique
from config.exceptions import PermissionDeniedException
from apps.user.models import User


class BasePermissions():

    # ------------ Define this after using this as base -----------
    @unique
    class Permission(Enum):
        pass
    __error_message__ = {}
    PERMISSION_MAP = {}
    CONTEXT_PERMISSION_ATTR = ''
    # ------------ Define this after using this as base -----------

    DEFAULT_PERMISSION_DENIED_MESSAGE = PermissionDeniedException.default_message

    @classmethod
    def get_permissions(cls, role):
        return cls.PERMISSION_MAP.get(role) or []

    @classmethod
    def get_permission_message(cls, permission):
        return cls.__error_message__.get(permission, cls.DEFAULT_PERMISSION_DENIED_MESSAGE)

    @classmethod
    def check_permission(cls, info, *perms):
        permissions = getattr(info.context, cls.CONTEXT_PERMISSION_ATTR)
        if permissions:
            return all([perm in permissions for perm in perms])

    @classmethod
    def check_permission_from_serializer(cls, context, *perms):
        permissions = getattr(context, cls.CONTEXT_PERMISSION_ATTR)
        if permissions:
            return all([perm in permissions for perm in perms])


class BookPermissions(BasePermissions):

    @unique
    class Permission(Enum):
        CREATE_BOOK = auto()
        UPDATE_BOOK = auto()
        DELETE_BOOK = auto()
        RETRIEVE_BOOK = auto()

    Permission.__name__ = 'BookPermission'

    __error_message__ = {
        Permission.CREATE_BOOK: "You don't have permission to create book",
        Permission.UPDATE_BOOK: "You don't have permission to update book",
        Permission.DELETE_BOOK: "You don't have permission to delete book",
        Permission.RETRIEVE_BOOK: "You don't have permission to retrieve book",
    }

    INDIVIDUAL_USER = [Permission.RETRIEVE_BOOK]
    SCHOOL_ADMIN = [*INDIVIDUAL_USER]
    PUBLISHER = [*INDIVIDUAL_USER, Permission.CREATE_BOOK, Permission.UPDATE_BOOK, Permission.DELETE_BOOK]
    INSTITUTIONAL_USER = [*INDIVIDUAL_USER]
    ADMIN = [*PUBLISHER]

    PERMISSION_MAP = {
        User.UserType.ADMIN: ADMIN,
        User.UserType.PUBLISHER: PUBLISHER,
        User.UserType.INSTITUTIONAL_USER: INSTITUTIONAL_USER,
        User.UserType.SCHOOL_ADMIN: SCHOOL_ADMIN,
        User.UserType.INDIVIDUAL_USER: INDIVIDUAL_USER,
    }

    CONTEXT_PERMISSION_ATTR = 'book_permissions'

    @classmethod
    def get_permissions(cls, role, is_public=False):
        return cls.PERMISSION_MAP.get(role) or []


class PublisherPermissions(BasePermissions):

    @unique
    class Permission(Enum):
        CREATE_PUBLISHER = auto()
        UPDATE_PUBLISHER = auto()
        DELETE_PUBLISHER = auto()
        RETRIEVE_PUBLISHER = auto()

    Permission.__name__ = 'PublisherPermission'

    __error_message__ = {
        Permission.CREATE_PUBLISHER: "You don't have permission to create publihser",
        Permission.UPDATE_PUBLISHER: "You don't have permission to update publihser",
        Permission.DELETE_PUBLISHER: "You don't have permission to delete publihser",
        Permission.RETRIEVE_PUBLISHER: "You don't have permission to retrieve publihser",
    }

    INDIVIDUAL_USER = [Permission.RETRIEVE_PUBLISHER]
    SCHOOL_ADMIN = [*INDIVIDUAL_USER]
    PUBLISHER = [*INDIVIDUAL_USER, Permission.UPDATE_PUBLISHER]
    INSTITUTIONAL_USER = [*INDIVIDUAL_USER]
    ADMIN = [*PUBLISHER, Permission.CREATE_PUBLISHER, Permission.DELETE_PUBLISHER]

    PERMISSION_MAP = {
        User.UserType.ADMIN: ADMIN,
        User.UserType.PUBLISHER: PUBLISHER,
        User.UserType.INSTITUTIONAL_USER: INSTITUTIONAL_USER,
        User.UserType.SCHOOL_ADMIN: SCHOOL_ADMIN,
        User.UserType.INDIVIDUAL_USER: INDIVIDUAL_USER,
    }

    CONTEXT_PERMISSION_ATTR = 'publisher_permissions'

    @classmethod
    def get_permissions(cls, role, is_public=False):
        return cls.PERMISSION_MAP.get(role) or []


class SchoolPermissions(BasePermissions):

    @unique
    class Permission(Enum):
        CREATE_SCHOOL = auto()
        UPDATE_SCHOOL = auto()
        DELETE_SCHOOL = auto()
        RETRIEVE_SCHOOL = auto()

    Permission.__name__ = 'SchoolPermission'

    __error_message__ = {
        Permission.CREATE_SCHOOL: "You don't have permission to create school",
        Permission.UPDATE_SCHOOL: "You don't have permission to update school",
        Permission.DELETE_SCHOOL: "You don't have permission to delete school",
        Permission.RETRIEVE_SCHOOL: "You don't have permission to retrieve school",
    }

    INDIVIDUAL_USER = [Permission.RETRIEVE_SCHOOL]
    SCHOOL_ADMIN = [*INDIVIDUAL_USER, Permission.UPDATE_SCHOOL]
    PUBLISHER = [*INDIVIDUAL_USER]
    INSTITUTIONAL_USER = [*INDIVIDUAL_USER]
    ADMIN = [*PUBLISHER, Permission.CREATE_SCHOOL, Permission.DELETE_SCHOOL]

    PERMISSION_MAP = {
        User.UserType.ADMIN: ADMIN,
        User.UserType.PUBLISHER: PUBLISHER,
        User.UserType.INSTITUTIONAL_USER: INSTITUTIONAL_USER,
        User.UserType.SCHOOL_ADMIN: SCHOOL_ADMIN,
        User.UserType.INDIVIDUAL_USER: INDIVIDUAL_USER,
    }

    CONTEXT_PERMISSION_ATTR = 'school_admin_permissions'

    @classmethod
    def get_permissions(cls, role, is_public=False):
        return cls.PERMISSION_MAP.get(role) or []


class InstitutionPermissions(BasePermissions):

    @unique
    class Permission(Enum):
        CREATE_INSTITUTION = auto()
        UPDATE_INSTITUTION = auto()
        DELETE_INSTITUTION = auto()
        RETRIEVE_INSTITUTION = auto()

    Permission.__name__ = 'InstitutionPermission'

    __error_message__ = {
        Permission.CREATE_INSTITUTION: "You don't have permission to create institution",
        Permission.UPDATE_INSTITUTION: "You don't have permission to update institution",
        Permission.DELETE_INSTITUTION: "You don't have permission to delete institution",
        Permission.RETRIEVE_INSTITUTION: "You don't have permission to retrieve institution",
    }

    INDIVIDUAL_USER = [Permission.RETRIEVE_INSTITUTION]
    SCHOOL_ADMIN = [*INDIVIDUAL_USER]
    PUBLISHER = [*INDIVIDUAL_USER]
    INSTITUTIONAL_USER = [*INDIVIDUAL_USER, Permission.UPDATE_INSTITUTION]
    ADMIN = [*PUBLISHER, Permission.CREATE_INSTITUTION, Permission.DELETE_INSTITUTION]

    PERMISSION_MAP = {
        User.UserType.ADMIN: ADMIN,
        User.UserType.PUBLISHER: PUBLISHER,
        User.UserType.INSTITUTIONAL_USER: INSTITUTIONAL_USER,
        User.UserType.SCHOOL_ADMIN: SCHOOL_ADMIN,
        User.UserType.INDIVIDUAL_USER: INDIVIDUAL_USER,
    }

    CONTEXT_PERMISSION_ATTR = 'institution_permissions'

    @classmethod
    def get_permissions(cls, role, is_public=False):
        return cls.PERMISSION_MAP.get(role) or []
