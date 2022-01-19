from django.utils.functional import cached_property

from utils.graphene.dataloaders import WithContextMixin

from apps.order.dataloaders import DataLoaders as OrderDataloader


class GlobalDataLoaders(WithContextMixin):
    @cached_property
    def cart_item(self):
        return OrderDataloader(context=self.context)
