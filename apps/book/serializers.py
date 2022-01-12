from rest_framework import serializers
# from django.utils.translation import ugettext as _

from apps.book.models import Book


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = '__all__'
