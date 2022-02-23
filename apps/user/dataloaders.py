from promise import Promise
from django.utils.functional import cached_property
from django.db import models

from utils.graphene.dataloaders import DataLoaderWithContext, WithContextMixin
from apps.book.models import Book

from .models import User


class WishListLoader(DataLoaderWithContext):
    def batch_load_fn(self, keys):
        book_qs = Book.objects.filter(id__in=keys).values_list('id', 'book_wish_list__id')
        wishlist_ids = {
            id: wish_list_id
            for id, wish_list_id in book_qs
        }
        return Promise.resolve([wishlist_ids.get(key) for key in keys])


class UserCanonicalNameLoader(DataLoaderWithContext):
    def batch_load_fn(self, keys):
        canonical_name_stat = models.functions.Coalesce(
            models.Case(
                *[
                    models.When(
                        user_type=user_type,
                        then=models.F(user_type_name)
                    ) for user_type, user_type_name in [
                        (User.UserType.PUBLISHER, 'publisher__name'),
                        (User.UserType.INSTITUTIONAL_USER, 'institution__name'),
                        (User.UserType.SCHOOL_ADMIN, 'school__name'),
                    ]
                ]
            ), models.F('full_name'), output_field=models.CharField(),
        )
        qs = User.objects\
            .filter(id__in=keys)\
            .annotate(canonical_name=canonical_name_stat)\
            .values_list('id', 'canonical_name')
        names_map = {id: name for id, name in qs}
        return Promise.resolve([names_map.get(key) for key in keys])


class DataLoaders(WithContextMixin):
    @cached_property
    def wishlist_id(self):
        return WishListLoader(context=self.context)

    @cached_property
    def canonical_name(self):
        return UserCanonicalNameLoader(context=self.context)
