import graphene
from utils.graphene.mutation import (
    generate_input_type_for_serializer,
    CreateUpdateGrapheneMutation,
    DeleteMutation
)

from apps.user.models import User
from apps.book.models import (
    Book,
    WishList,
    Tag,
    Category,
    Author,
)
from apps.book.schema import (
    BookType,
    WishListType,
    TagType,
    CategoryType,
    AuthorType,
)
from apps.book.serializers import (
    BookSerializer,
    WishListSerializer,
    BookTagSerializer,
    BookCategorySerializer,
    BookAuthorSerializer,
)
from config.permissions import UserPermissions


BookInputType = generate_input_type_for_serializer(
    'BookCreateInputType',
    serializer_class=BookSerializer
)


class BookMutationMixin():
    @classmethod
    def filter_queryset(cls, qs, info):
        if info.context.user.user_type == User.UserType.PUBLISHER.value:
            return qs.filter(publisher=info.context.user.publisher)
        elif info.context.user.user_type == User.UserType.ADMIN.value:
            return qs
        return qs.none()


class BookAdminOnlyMutationMixin():
    @classmethod
    def filter_queryset(cls, qs, info):
        if info.context.user.user_type == User.UserType.ADMIN.value:
            return qs
        return qs.none()


class BookAdminAndAuthorMutationMixin():
    @classmethod
    def filter_queryset(cls, qs, info):
        if info.context.user.user_type in [User.UserType.ADMIN.value, User.UserType.PUBLISHER.value]:
            return qs
        return qs.none()


class CreateBook(BookMutationMixin, CreateUpdateGrapheneMutation):
    class Arguments:
        data = BookInputType(required=True)
    model = Book
    serializer_class = BookSerializer
    result = graphene.Field(BookType)
    permissions = [UserPermissions.Permission.CAN_CREATE_BOOK]


class UpdateBook(BookMutationMixin, CreateUpdateGrapheneMutation):
    class Arguments:
        data = BookInputType(required=True)
        id = graphene.ID(required=True)
    model = Book
    serializer_class = BookSerializer
    result = graphene.Field(BookType)
    permissions = [UserPermissions.Permission.CAN_UPDATE_BOOK]


class DeleteBook(BookMutationMixin, DeleteMutation):
    class Arguments:
        id = graphene.ID(required=True)
    model = Book
    result = graphene.Field(BookType)
    permissions = [UserPermissions.Permission.CAN_DELETE_BOOK]


WishListInputType = generate_input_type_for_serializer(
    'WishListInputType',
    serializer_class=WishListSerializer
)


class WishListMixin():
    @classmethod
    def filter_queryset(cls, qs, info):
        return qs.filter(created_by=info.context.user)


class CreateWishList(WishListMixin, CreateUpdateGrapheneMutation):
    class Arguments:
        data = WishListInputType(required=True)
    model = WishList
    serializer_class = WishListSerializer
    result = graphene.Field(WishListType)

    @classmethod
    def check_permissions(cls, *args, **_):
        return True


class DeleteWishList(WishListMixin, DeleteMutation):
    class Arguments:
        id = graphene.ID(required=True)
    model = WishList
    result = graphene.Field(WishListType)

    @classmethod
    def check_permissions(cls, *args, **_):
        return True


BookTagInputType = generate_input_type_for_serializer(
    'BookTagInputType',
    serializer_class=BookTagSerializer
)


class CreateBookTag(BookAdminOnlyMutationMixin, CreateUpdateGrapheneMutation):
    class Arguments:
        data = BookTagInputType(required=True)
    model = Tag
    serializer_class = BookTagSerializer
    result = graphene.Field(TagType)
    permissions = [UserPermissions.Permission.CAN_CREATE_BOOK_TAG]


class UpdateBookTag(BookAdminOnlyMutationMixin, CreateUpdateGrapheneMutation):
    class Arguments:
        data = BookTagInputType(required=True)
        id = graphene.ID(required=True)
    model = Tag
    serializer_class = BookTagSerializer
    result = graphene.Field(TagType)
    permissions = [UserPermissions.Permission.CAN_UPDATE_BOOK_TAG]


class DeleteBookTag(BookAdminOnlyMutationMixin, DeleteMutation):
    class Arguments:
        id = graphene.ID(required=True)
    model = Tag
    result = graphene.Field(TagType)
    permissions = [UserPermissions.Permission.CAN_DELETE_BOOK_TAG]


BookCategoryInputType = generate_input_type_for_serializer(
    'BookCategoryInputType',
    serializer_class=BookCategorySerializer
)


class CreateBookCategory(BookAdminOnlyMutationMixin, CreateUpdateGrapheneMutation):
    class Arguments:
        data = BookCategoryInputType(required=True)
    model = Category
    serializer_class = BookCategorySerializer
    result = graphene.Field(CategoryType)
    permissions = [UserPermissions.Permission.CAN_CREATE_BOOK_CATEGORY]


class UpdateBookCategory(BookAdminOnlyMutationMixin, CreateUpdateGrapheneMutation):
    class Arguments:
        data = BookCategoryInputType(required=True)
        id = graphene.ID(required=True)
    model = Category
    serializer_class = BookCategorySerializer
    result = graphene.Field(CategoryType)
    permissions = [UserPermissions.Permission.CAN_UPDATE_BOOK_CATEGORY]


class DeleteBookCategory(BookAdminOnlyMutationMixin, DeleteMutation):
    class Arguments:
        id = graphene.ID(required=True)
    model = Category
    result = graphene.Field(CategoryType)
    permissions = [UserPermissions.Permission.CAN_DELETE_BOOK_CATEGORY]


BookAuthorInputType = generate_input_type_for_serializer(
    'BookAuthorInputType',
    serializer_class=BookAuthorSerializer
)


class CreateBookAuthor(BookAdminAndAuthorMutationMixin, CreateUpdateGrapheneMutation):
    class Arguments:
        data = BookAuthorInputType(required=True)
    model = Author
    serializer_class = BookAuthorSerializer
    result = graphene.Field(AuthorType)
    permissions = [UserPermissions.Permission.CAN_CREATE_BOOK_AUTHOR]


class UpdateBookAuthor(BookAdminAndAuthorMutationMixin, CreateUpdateGrapheneMutation):
    class Arguments:
        data = BookAuthorInputType(required=True)
        id = graphene.ID(required=True)
    model = Author
    serializer_class = BookAuthorSerializer
    result = graphene.Field(AuthorType)
    permissions = [UserPermissions.Permission.CAN_UPDATE_BOOK_AUTHOR]


class DeleteBookAuthor(BookAdminOnlyMutationMixin, DeleteMutation):
    class Arguments:
        id = graphene.ID(required=True)
    model = Author
    result = graphene.Field(AuthorType)
    permissions = [UserPermissions.Permission.CAN_DELETE_BOOK_AUTHOR]


class Mutation(graphene.ObjectType):
    create_book = CreateBook.Field()
    update_book = UpdateBook.Field()
    delete_book = DeleteBook.Field()
    create_wishlist = CreateWishList.Field()
    delete_wishList = DeleteWishList.Field()
    create_book_tag = CreateBookTag.Field()
    update_book_tag = UpdateBookTag.Field()
    delete_book_tag = DeleteBookTag.Field()
    create_book_category = CreateBookCategory.Field()
    update_book_category = UpdateBookCategory.Field()
    delete_book_category = DeleteBookCategory.Field()
    create_book_author = CreateBookAuthor.Field()
    update_book_author = UpdateBookAuthor.Field()
    delete_book_author = DeleteBookAuthor.Field()
