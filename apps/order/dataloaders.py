from collections import defaultdict
from django.db import models
from promise import Promise
from django.utils.functional import cached_property
from .models import CartItem, BookOrder
from utils.graphene.dataloaders import DataLoaderWithContext, WithContextMixin


class TotalPriceLoader(DataLoaderWithContext):
    def batch_load_fn(self, keys):
        cart_items_qs = CartItem.objects.filter(id__in=keys).annotate(
            total_price=models.F('book__price') * models.F('quantity')
        ).values_list('id', 'total_price')
        total_price = {
            id: total_price
            for id, total_price in cart_items_qs
        }
        return Promise.resolve([total_price.get(key, 0) for key in keys])


class BookOrdersLoader(DataLoaderWithContext):
    def batch_load_fn(self, keys):
        book_order_qs = BookOrder.objects.filter(order__in=keys)
        _map = defaultdict(list)
        for book_order in book_order_qs:
            _map[book_order.order_id].append(book_order)

        return Promise.resolve([_map[key] for key in keys])


class DataLoaders(WithContextMixin):
    @cached_property
    def total_price(self):
        return TotalPriceLoader(context=self.context)

    @cached_property
    def book_orders(self):
        return BookOrdersLoader(context=self.context)
