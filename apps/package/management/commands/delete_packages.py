from django.db import transaction
from django.core.management.base import BaseCommand
from apps.order.models import OrderWindow
from apps.package.models import (
    PublisherPackage,
    SchoolPackage,
    InstitutionPackage,
    CourierPackage,
)

INCENTIVE_LIMIT = 10


class Command(BaseCommand):
    help = 'Delete package of particular order window'

    def add_arguments(self, parser):
        parser.add_argument('order_window_id', type=int, help='order window id')

    @transaction.atomic
    def handle(self, *args, **options):
        order_window_id = options['order_window_id']
        order_window_id = options['order_window_id']
        # Check if order window exists
        try:
            order_window = OrderWindow.objects.get(id=order_window_id)
        except OrderWindow.DoesNotExist:
            self.stdout.write(self.style.ERROR('Invalid order window id supplied.'))
            return

        school_packages = SchoolPackage.objects.filter(order_window=order_window)
        for school_package in school_packages:
            school_package.school_package.all().delete()
        school_packages.delete()

        publisher_packages = PublisherPackage.objects.filter(order_window=order_window)
        for publisher_package in publisher_packages:
            publisher_package.publisher_package.all().delete()
        publisher_packages.delete()

        institution_packages = InstitutionPackage.objects.filter(order_window=order_window)
        for institution_package in institution_packages:
            institution_package.institution_package.all().delete()
        institution_packages.delete()

        courier_packages = CourierPackage.objects.filter(order_window=order_window)
        courier_packages.delete()
        self.stdout.write(self.style.SUCCESS(
            f'Deleted {order_window} packages.'
        ))
