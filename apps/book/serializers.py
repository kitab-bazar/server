from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _

from apps.book.models import Book, WishList


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = '__all__'


class WishListSerializer(serializers.ModelSerializer):

    class Meta:
        model = WishList
        fields = ('book', )

    def validate(self, attrs):
        request = self.context.get('request')
        attrs['user'] = request.user
        book = attrs.get('book', None)
        if WishList.objects.filter(user=request.user, book=book).exists():
            raise serializers.ValidationError(_('Book is already added in wish list.'))
        return attrs
