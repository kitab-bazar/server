from enum import Enum, auto, unique
from config.exceptions import PermissionDeniedException
from apps.user.models import User


class UserPermissions():

    DEFAULT_PERMISSION_DENIED_MESSAGE = PermissionDeniedException.default_message

    @unique
    class Permission(Enum):
        CAN_CREATE_BOOK = auto()
        CAN_UPDATE_BOOK = auto()
        CAN_DELETE_BOOK = auto()
        CAN_RETRIEVE_BOOK = auto()

        CAN_CREATE_BOOK_CATEGORY = auto()
        CAN_UPDATE_BOOK_CATEGORY = auto()
        CAN_DELETE_BOOK_CATEGORY = auto()
        CAN_RETRIEVE_BOOK_CATEGORY = auto()

        CAN_CREATE_BOOK_AUTHOR = auto()
        CAN_UPDATE_BOOK_AUTHOR = auto()
        CAN_DELETE_BOOK_AUTHOR = auto()
        CAN_RETRIEVE_BOOK_AUTHOR = auto()

        CAN_CREATE_BOOK_TAG = auto()
        CAN_UPDATE_BOOK_TAG = auto()
        CAN_DELETE_BOOK_TAG = auto()
        CAN_RETRIEVE_BOOK_TAG = auto()

        CAN_CREATE_PUBLISHER = auto()
        CAN_UPDATE_PUBLISHER = auto()
        CAN_DELETE_PUBLISHER = auto()
        CAN_RETRIEVE_PUBLISHER = auto()

        CAN_CREATE_SCHOOL = auto()
        CAN_UPDATE_SCHOOL = auto()
        CAN_DELETE_SCHOOL = auto()
        CAN_RETRIEVE_SCHOOL = auto()

        CAN_CREATE_INSTITUTION = auto()
        CAN_UPDATE_INSTITUTION = auto()
        CAN_DELETE_INSTITUTION = auto()
        CAN_RETRIEVE_INSTITUTION = auto()

        CREATE_ORDER = auto()
        UPDATE_ORDER = auto()
        DELETE_ORDER = auto()
        RETRIEVE_ORDER = auto()

        CREATE_FAQ = auto()
        UPDATE_FAQ = auto()
        DELETE_FAQ = auto()
        RETRIEVE_FAQ = auto()

        CREATE_CONTACT_MESSAGE = auto()
        UPDATE_CONTACT_MESSAGE = auto()
        DELETE_CONTACT_MESSAGE = auto()
        RETRIEVE_CONTACT_MESSAGE = auto()
        CAN_CREATE_BLOG = auto()
        CAN_UPDATE_BLOG = auto()
        CAN_DELETE_BLOG = auto()
        CAN_RETRIEVE_BLOG = auto()

        CAN_CREATE_BLOG_CATEGORY = auto()
        CAN_UPDATE_BLOG_CATEGORY = auto()
        CAN_DELETE_BLOG_CATEGORY = auto()
        CAN_RETRIEVE_BLOG_CATEGORY = auto()

        CAN_CREATE_BLOG_TAG = auto()
        CAN_UPDATE_BLOG_TAG = auto()
        CAN_DELETE_BLOG_TAG = auto()
        CAN_RETRIEVE_BLOG_TAG = auto()

        CAN_VERIFY_USER = auto()

    Permission.__name__ = 'UserPermissions'

    __error_message__ = {
        Permission.CAN_CREATE_BOOK: "You don't have permission to create book",
        Permission.CAN_UPDATE_BOOK: "You don't have permission to update book",
        Permission.CAN_DELETE_BOOK: "You don't have permission to delete book",
        Permission.CAN_RETRIEVE_BOOK: "You don't have permission to retrieve book",

        Permission.CAN_CREATE_BOOK_CATEGORY: "You don't have permission to create book category",
        Permission.CAN_UPDATE_BOOK_CATEGORY: "You don't have permission to update book category",
        Permission.CAN_DELETE_BOOK_CATEGORY: "You don't have permission to delete book category",
        Permission.CAN_RETRIEVE_BOOK_CATEGORY: "You don't have permission to retrieve book category",

        Permission.CAN_CREATE_BOOK_AUTHOR: "You don't have permission to create book author",
        Permission.CAN_UPDATE_BOOK_AUTHOR: "You don't have permission to update book author",
        Permission.CAN_DELETE_BOOK_AUTHOR: "You don't have permission to delete book author",
        Permission.CAN_RETRIEVE_BOOK_AUTHOR: "You don't have permission to retrieve book author",

        Permission.CAN_CREATE_BOOK_TAG: "You don't have permission to create book tag",
        Permission.CAN_UPDATE_BOOK_TAG: "You don't have permission to update book tag",
        Permission.CAN_DELETE_BOOK_TAG: "You don't have permission to delete book tag",
        Permission.CAN_RETRIEVE_BOOK_TAG: "You don't have permission to retrieve book tag",

        Permission.CAN_CREATE_PUBLISHER: "You don't have permission to create publihser",
        Permission.CAN_UPDATE_PUBLISHER: "You don't have permission to update publihser",
        Permission.CAN_DELETE_PUBLISHER: "You don't have permission to delete publihser",
        Permission.CAN_RETRIEVE_PUBLISHER: "You don't have permission to retrieve publihser",

        Permission.CAN_CREATE_SCHOOL: "You don't have permission to create school",
        Permission.CAN_UPDATE_SCHOOL: "You don't have permission to update school",
        Permission.CAN_DELETE_SCHOOL: "You don't have permission to delete school",
        Permission.CAN_RETRIEVE_SCHOOL: "You don't have permission to retrieve school",

        Permission.CAN_CREATE_INSTITUTION: "You don't have permission to create institution",
        Permission.CAN_UPDATE_INSTITUTION: "You don't have permission to update institution",
        Permission.CAN_DELETE_INSTITUTION: "You don't have permission to delete institution",
        Permission.CAN_RETRIEVE_INSTITUTION: "You don't have permission to retrieve institution",

        Permission.CREATE_ORDER: "You don't have permission to create order",
        Permission.UPDATE_ORDER: "You don't have permission to update order",
        Permission.DELETE_ORDER: "You don't have permission to delete order",
        Permission.RETRIEVE_ORDER: "You don't have permission to retrieve order",

        Permission.CREATE_FAQ: "You don't have permission to create faq.",
        Permission.UPDATE_FAQ: "You don't have permission to update faq.",
        Permission.DELETE_FAQ: "You don't have permission to delete faq.",
        Permission.RETRIEVE_FAQ: "You don't have permission to retrieve faq.",

        Permission.CREATE_CONTACT_MESSAGE: "You don't have permission to create contact message.",
        Permission.UPDATE_CONTACT_MESSAGE: "You don't have permission to update contact message.",
        Permission.DELETE_CONTACT_MESSAGE: "You don't have permission to delete contact message.",
        Permission.RETRIEVE_CONTACT_MESSAGE: "You don't have permission to retrieve contact message.",

        Permission.CAN_CREATE_BLOG: "You don't have permission to create blog",
        Permission.CAN_UPDATE_BLOG: "You don't have permission to update blog",
        Permission.CAN_DELETE_BLOG: "You don't have permission to delete blog",
        Permission.CAN_RETRIEVE_BLOG: "You don't have permission to retrieve blog",

        Permission.CAN_CREATE_BLOG_CATEGORY: "You don't have permission to create blog category",
        Permission.CAN_UPDATE_BLOG_CATEGORY: "You don't have permission to update blog category",
        Permission.CAN_DELETE_BLOG_CATEGORY: "You don't have permission to delete blog category",
        Permission.CAN_RETRIEVE_BLOG_CATEGORY: "You don't have permission to retrieve blog category",

        Permission.CAN_CREATE_BLOG_TAG: "You don't have permission to create blog tag",
        Permission.CAN_UPDATE_BLOG_TAG: "You don't have permission to update blog tag",
        Permission.CAN_DELETE_BLOG_TAG: "You don't have permission to delete blog tag",
        Permission.CAN_RETRIEVE_BLOG_TAG: "You don't have permission to retrieve blog tag",

        Permission.CAN_VERIFY_USER: "You don't have permission to verify user",
    }

    INDIVIDUAL_USER = [
        Permission.CAN_RETRIEVE_BOOK,
        Permission.CAN_RETRIEVE_PUBLISHER,
        Permission.CAN_RETRIEVE_SCHOOL,
        Permission.CAN_RETRIEVE_INSTITUTION,
        Permission.CREATE_ORDER,
        Permission.RETRIEVE_ORDER,
        Permission.RETRIEVE_FAQ,
        Permission.CREATE_CONTACT_MESSAGE,
        Permission.CAN_RETRIEVE_BOOK_CATEGORY,
        Permission.CAN_RETRIEVE_BOOK_TAG,
        Permission.CAN_RETRIEVE_BOOK_AUTHOR,
        Permission.CAN_RETRIEVE_BLOG,
        Permission.CAN_RETRIEVE_BLOG_CATEGORY,
        Permission.CAN_RETRIEVE_BLOG_TAG,
    ]

    SCHOOL_ADMIN = [
        *INDIVIDUAL_USER,
        Permission.CAN_UPDATE_SCHOOL,
        Permission.UPDATE_ORDER,
    ]

    PUBLISHER = [
        *INDIVIDUAL_USER, Permission.CAN_CREATE_BOOK,
        Permission.CAN_UPDATE_BOOK,
        Permission.CAN_DELETE_BOOK,
        Permission.CAN_UPDATE_PUBLISHER,
        Permission.UPDATE_ORDER,
        Permission.DELETE_ORDER,
        Permission.CAN_CREATE_BOOK_AUTHOR,
        Permission.CAN_UPDATE_BOOK_AUTHOR,
    ]

    INSTITUTIONAL_USER = [*INDIVIDUAL_USER, Permission.CAN_UPDATE_INSTITUTION]

    MODERATOR = [
        *INDIVIDUAL_USER, *PUBLISHER, *INSTITUTIONAL_USER, *SCHOOL_ADMIN,
        Permission.CAN_DELETE_BLOG_TAG,
        Permission.CAN_CREATE_PUBLISHER,
        Permission.CAN_DELETE_PUBLISHER,
        Permission.CAN_CREATE_SCHOOL,
        Permission.CAN_DELETE_SCHOOL,
        Permission.CAN_CREATE_INSTITUTION,
        Permission.CAN_DELETE_INSTITUTION,
        Permission.CREATE_FAQ,
        Permission.UPDATE_FAQ,
        Permission.DELETE_FAQ,
        Permission.RETRIEVE_CONTACT_MESSAGE,
        Permission.UPDATE_CONTACT_MESSAGE,
        Permission.DELETE_CONTACT_MESSAGE,
        Permission.CAN_CREATE_BOOK_TAG,
        Permission.CAN_UPDATE_BOOK_TAG,
        Permission.CAN_DELETE_BOOK_TAG,
        Permission.CAN_CREATE_BOOK_CATEGORY,
        Permission.CAN_UPDATE_BOOK_CATEGORY,
        Permission.CAN_DELETE_BOOK_CATEGORY,
        Permission.CAN_DELETE_BOOK_AUTHOR,
        Permission.CAN_DELETE_BLOG,
        Permission.CAN_CREATE_BLOG,
        Permission.CAN_DELETE_BLOG,
        Permission.CAN_UPDATE_BLOG,
        Permission.CAN_CREATE_BLOG_CATEGORY,
        Permission.CAN_UPDATE_BLOG_CATEGORY,
        Permission.CAN_DELETE_BLOG_CATEGORY,
        Permission.CAN_CREATE_BLOG_TAG,
        Permission.CAN_UPDATE_BLOG_TAG,
        Permission.CAN_VERIFY_USER,
    ]

    # ----------------------------------------
    # Remove special permission from publisher
    # -----------------------------------------
    PUBLISHER = list(set(PUBLISHER) - set([
        Permission.CREATE_ORDER]
    ))

    PERMISSION_MAP = {
        User.UserType.MODERATOR: MODERATOR,
        User.UserType.PUBLISHER: PUBLISHER,
        User.UserType.INSTITUTIONAL_USER: INSTITUTIONAL_USER,
        User.UserType.SCHOOL_ADMIN: SCHOOL_ADMIN,
        User.UserType.INDIVIDUAL_USER: INDIVIDUAL_USER,
    }

    CONTEXT_PERMISSION_ATTR = 'user_permissions'

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

    @classmethod
    def get_permissions(cls, role, is_public=False):
        return list(set(cls.PERMISSION_MAP.get(role))) or []
