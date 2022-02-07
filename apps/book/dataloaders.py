from promise import Promise
from django.utils.functional import cached_property

from utils.graphene.dataloaders import DataLoaderWithContext, WithContextMixin
from apps.book.models import Book
from apps.order.models import CartItem


class WishListLoader(DataLoaderWithContext):
    def batch_load_fn(self, keys):
        book_qs = Book.objects.filter(id__in=keys).values_list('id', 'book_wish_list__id')
        wishlist_ids = {
            id: wish_list_id
            for id, wish_list_id in book_qs
        }
        return Promise.resolve([wishlist_ids.get(key) for key in keys])


class CartDetailsLoader(DataLoaderWithContext):
    def batch_load_fn(self, keys):
        book_qs = Book.objects.filter(id__in=keys).values_list('id', 'book_cart_item')
        cart_details_qs = {}
        for id, cart_id in book_qs:
            cart = None
            if cart_id:
                cart = CartItem.objects.get(id=cart_id)
            cart_details_qs.update({id: cart})

        return Promise.resolve([cart_details_qs.get(key) for key in keys])


class DataLoaders(WithContextMixin):

    @cached_property
    def wishlist_id(self):
        return WishListLoader(context=self.context)

    @cached_property
    def cart_details(self):
        return CartDetailsLoader(context=self.context)
