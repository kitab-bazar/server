import graphene
from utils.graphene.mutation import (
    generate_input_type_for_serializer,
    CreateUpdateGrapheneMutation,
    DeleteMutation
)

from apps.user.models import User
from apps.book.models import Book, WishList
from apps.book.schema import BookType, WishListType
from apps.book.serializers import BookSerializer, WishListSerializer
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
        return Book.objects.none()


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


class Mutation(graphene.ObjectType):
    create_book = CreateBook.Field()
    update_book = UpdateBook.Field()
    delete_book = DeleteBook.Field()
    create_wishlist = CreateWishList.Field()
    delete_wishList = DeleteWishList.Field()
