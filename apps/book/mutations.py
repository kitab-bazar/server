import graphene
from django.utils.translation import ugettext as _

from utils.graphene.mutation import generate_input_type_for_serializer
from utils.graphene.error_types import CustomErrorType, mutation_is_not_valid

from apps.book.models import Book
from apps.book.schema import BookType
from apps.book.serializers import BookSerializer


BookInputType = generate_input_type_for_serializer(
    'BookCreateInputType',
    serializer_class=BookSerializer
)


class CreateBook(graphene.Mutation):
    class Arguments:
        data = BookInputType(required=True)

    errors = graphene.List(graphene.NonNull(CustomErrorType))
    ok = graphene.Boolean()
    result = graphene.Field(BookType)

    @staticmethod
    def mutate(root, info, data):
        serializer = BookSerializer(data=data, context={'request': info.context.request})
        if errors := mutation_is_not_valid(serializer):
            return CreateBook(errors=errors, ok=False)
        instance = serializer.save()
        return CreateBook(result=instance, errors=None, ok=True)


class UpdateBook(graphene.Mutation):
    class Arguments:
        data = BookInputType(required=True)
        id = graphene.ID(required=True)

    errors = graphene.List(graphene.NonNull(CustomErrorType))
    ok = graphene.Boolean()
    result = graphene.Field(BookType)

    @staticmethod
    def mutate(root, info, data):
        try:
            instance = Book.objects.get(id=data['id'])
        except Book.DoesNotExist:
            return UpdateBook(errors=[
                dict(field='nonFieldErrors', messages=_('Book does not exist.'))
            ])
        serializer = BookSerializer(
            instance=instance, data=data,
            context={'request': info.context.request}, partial=True
        )
        if errors := mutation_is_not_valid(serializer):
            return UpdateBook(errors=errors, ok=False)
        instance = serializer.save()
        return UpdateBook(result=instance, errors=None, ok=True)


class DeleteBook(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    errors = graphene.List(graphene.NonNull(CustomErrorType))
    ok = graphene.Boolean()
    result = graphene.Field(BookType)

    @staticmethod
    def mutate(root, info, id):
        try:
            instance = Book.objects.get(id=id)
        except Book.DoesNotExist:
            return DeleteBook(errors=[
                dict(field='nonFieldErrors', messages=_('Book does not exist.'))
            ])
        instance.delete()
        instance.id = id
        return DeleteBook(result=instance, errors=None, ok=True)


class Mutation(graphene.ObjectType):
    create_book = CreateBook.Field()
    update_book = UpdateBook.Field()
    delete_book = DeleteBook.Field()
