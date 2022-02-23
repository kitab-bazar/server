from utils.graphene.enums import (
    convert_enum_to_graphene_enum,
    get_enum_name_from_django_field,
)

from apps.book.models import Book

BookGradeEnum = convert_enum_to_graphene_enum(Book.Grade, name='BookGradeEnum')
LanguageTypeEnum = convert_enum_to_graphene_enum(Book.LanguageType, name='LanguageTypeEnum')

enum_map = {
    get_enum_name_from_django_field(field): enum
    for field, enum in (
        (Book.grade, BookGradeEnum),
        (Book.language, LanguageTypeEnum),
    )
}
