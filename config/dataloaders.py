from django.utils.functional import cached_property

from utils.graphene.dataloaders import WithContextMixin

from apps.order.dataloaders import DataLoaders as OrderDataloader
from apps.book.dataloaders import DataLoaders as BookDataloader


class GlobalDataLoaders(WithContextMixin):
    @cached_property
    def cart_item(self):
        return OrderDataloader(context=self.context)

    @cached_property
    def book(self):
        return BookDataloader(context=self.context)