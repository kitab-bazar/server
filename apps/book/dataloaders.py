from django.db import models
from promise import Promise
from django.utils.functional import cached_property
from django.db.models.functions import Cast

from utils.graphene.dataloaders import DataLoaderWithContext, WithContextMixin
from apps.book.models import Book


class QuantityInCartLoader(DataLoaderWithContext):

    def batch_load_fn(self, keys):
        book_qs = Book.objects.filter(id__in=keys).values('book_cart_item').annotate(
            quantity=Cast(models.F('book_cart_item__quantity'), models.IntegerField())
        ).values_list('id', 'quantity')
        quantity_in_cart = {
            id: quantity or 0
            for id, quantity in book_qs
        }
        return Promise.resolve([quantity_in_cart.get(key, 0) for key in keys])


class WishListLoader(DataLoaderWithContext):
    def batch_load_fn(self, keys):
        book_qs = Book.objects.filter(id__in=keys).select_related(
            'book_wish_list'
        ).values_list('id', 'book_wish_list__id')
        wishlist_ids = {
            id: wish_list_id
            for id, wish_list_id in book_qs
        }
        return Promise.resolve([wishlist_ids.get(key, 0) for key in keys])


class DataLoaders(WithContextMixin):
    @cached_property
    def quantity_in_cart(self):
        return QuantityInCartLoader(context=self.context)

    @cached_property
    def wishlist_id(self):
        return WishListLoader(context=self.context)
