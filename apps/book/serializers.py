from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from apps.book.models import Book, WishList, Tag, Author, Category
from config.serializers import CreatedUpdatedBaseSerializer


class BookSerializer(CreatedUpdatedBaseSerializer, serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = (
            'id', 'categories', 'authors', 'tags', 'isbn', 'number_of_pages', 'price',
            'image', 'language', 'weight', 'published_date', 'edition', 'publisher',
            'grade', 'is_published',

            # English fields
            'title_en', 'description_en', 'meta_title_en', 'meta_keywords_en', 'meta_description_en',
            'og_title_en', 'og_description_en', 'og_locale_en', 'og_type_en',

            # Nepali fields
            'title_ne', 'description_ne', 'meta_title_ne', 'meta_keywords_ne', 'meta_description_ne',
            'og_title_ne', 'og_description_ne', 'og_locale_ne', 'og_type_ne',

        )


class WishListSerializer(CreatedUpdatedBaseSerializer, serializers.ModelSerializer):

    class Meta:
        model = WishList
        fields = ('book', )

    def validate_book(self, book):
        created_by = self.context['request'].user
        if WishList.objects.filter(created_by=created_by, book=book).exists():
            raise serializers.ValidationError(_('Book is already added in wish list.'))
        return book


class BookTagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = (
            'id', 'name_en', 'name_ne'
        )


class BookAuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = (
            'id', 'name_en', 'name_ne',
            'about_author_en', 'about_author_ne'
        )


class BookCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = (
            'id', 'name_en', 'name_ne'
        )
