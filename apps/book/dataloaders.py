from promise import Promise
from django.utils.functional import cached_property

from utils.graphene.dataloaders import DataLoaderWithContext, WithContextMixin
from apps.book.models import Book


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
    def wishlist_id(self):
        return WishListLoader(context=self.context)
