from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from apps.book.models import Book, WishList, Tag, Author, Category
from config.serializers import CreatedUpdatedBaseSerializer


class BookSerializer(CreatedUpdatedBaseSerializer, serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = '__all__'


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
        fields = '__all__'


class BookAuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = '__all__'


class BookCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'
