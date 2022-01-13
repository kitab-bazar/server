import graphene
from utils.graphene.mutation import (
    generate_input_type_for_serializer,
    CreateUpdateGrapheneMutation,
    DeleteMutation
)

from apps.book.models import Book
from apps.book.schema import BookType
from apps.book.serializers import BookSerializer


BookInputType = generate_input_type_for_serializer(
    'BookCreateInputType',
    serializer_class=BookSerializer
)


class CreateBook(CreateUpdateGrapheneMutation):
    class Arguments:
        data = BookInputType(required=True)
    model = Book
    serializer_class = BookSerializer
    result = graphene.Field(BookType)

    @classmethod
    def check_permissions(cls, *args, **_):
        return True


class UpdateBook(CreateUpdateGrapheneMutation):
    class Arguments:
        data = BookInputType(required=True)
        id = graphene.ID(required=True)
    model = Book
    serializer_class = BookSerializer
    result = graphene.Field(BookType)

    @classmethod
    def check_permissions(cls, *args, **_):
        return True


class DeleteBook(DeleteMutation):
    class Arguments:
        id = graphene.ID(required=True)
    model = Book
    result = graphene.Field(BookType)

    @classmethod
    def check_permissions(cls, *args, **_):
        return True


class Mutation(graphene.ObjectType):
    create_book = CreateBook.Field()
    update_book = UpdateBook.Field()
    delete_book = DeleteBook.Field()
