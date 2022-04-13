from promise import Promise
from django.utils.functional import cached_property
from apps.order.models import Order
from apps.notification.models import Notification
from utils.graphene.dataloaders import DataLoaderWithContext, WithContextMixin


class OrderLoader(DataLoaderWithContext):
    def batch_load_fn(self, keys):
        notifications_qs = Notification.objects.filter(
            id__in=keys
        ).values('id', 'object_id', 'content_type__model')
        # TODO: Find the way to retrieve content_object instead of object_id form GenericForeignKey
        orders = {}
        for item in notifications_qs:
            id = item['id']
            object_id = item['object_id']
            content_type__model = item['content_type__model']
            orders[id] = None
            if content_type__model == Order.__name__.lower():
                try:
                    orders[id] = Order.objects.get(id=object_id)
                except Order.DoesNotExist:
                    pass
        return Promise.resolve([orders.get(key, 0) for key in keys])


class DataLoaders(WithContextMixin):
    @cached_property
    def order(self):
        return OrderLoader(context=self.context)
