from django.db import models
from promise import Promise
from django.utils.functional import cached_property

from utils.graphene.dataloaders import DataLoaderWithContext, WithContextMixin
from apps.book.models import Book


class QuantityInCartLoader(DataLoaderWithContext):
    def batch_load_fn(self, keys):
        book_qs = Book.objects.filter(id__in=keys).values('book_cart_item').annotate(
            quantity=models.F('book_cart_item__quantity')
        ).values_list('id', 'quantity')
        quantity_in_cart = {
            id: quantity
            for id, quantity in book_qs
        }
        return Promise.resolve([quantity_in_cart.get(key, 0) for key in keys])


class DataLoaders(WithContextMixin):
    @cached_property
    def quantity_in_cart(self):
        return QuantityInCartLoader(context=self.context)
