from rest_framework import serializers
from django.db.models import F

from apps.order.models import CartItem
from config.serializers import CreatedUpdatedBaseSerializer


class CartItemSerializer(CreatedUpdatedBaseSerializer, serializers.ModelSerializer):

    class Meta:
        model = CartItem
        fields = ('book', 'quantity',)

    def create(self, validated_data):
        created_by = self.context['request'].user
        validated_data['created_by'] = created_by
        book = validated_data.get('book', '')
        quantity = validated_data.get('quantity', '')
        # Update quantity in cart if book is already in cart
        if CartItem.objects.filter(created_by=created_by, book=book).exists():
            return CartItem.objects.filter(created_by=created_by, book=book).update(quantity=F('quantity') + quantity)
        else:
            # Otherwise create new cart item
            return CartItem.objects.create(**validated_data)
