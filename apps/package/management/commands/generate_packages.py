from django.core.management.base import BaseCommand
from apps.publisher.models import Publisher
from apps.order.models import Order, OrderWindow
from apps.package.models import PublisherPackage, PublisherPackageBook, SchoolPackage, SchoolPackageBook, CourierPackage
from apps.user.models import User


class Command(BaseCommand):
    help = 'Generate publisher packages'

    def handle(self, *args, **options):
        # ------------------------------------------------------------------
        # Create publihser packages
        # ------------------------------------------------------------------
        # Get latest order window
        latest_order_window = OrderWindow.objects.last()

        if not latest_order_window:
            self.stdout.write(self.style.ERROR('Active order window does not exist.'))
            return

        # Get orders in latest order window
        orders = Order.objects.filter(
            book_order__publisher__isnull=False,
            assigned_order_window__id=latest_order_window.id,
            status=Order.Status.PENDING.value
        )

        # Get unique publishers in order
        publisher_ids = orders.values_list('book_order__publisher', flat=True).distinct()

        publisher_package_count = 0

        # Create packages for each publishers
        for publisher_id in publisher_ids:
            publisher = Publisher.objects.get(id=publisher_id)
            related_orders = orders.filter(book_order__publisher=publisher)
            package = PublisherPackage.objects.create(
                status=PublisherPackage.Status.PENDING.value, publisher=publisher
            )
            package.related_orders.set(related_orders)
            PublisherPackageBook.objects.bulk_create(
                [
                    PublisherPackageBook(
                        book_id=related_book_order['book_order__book'],
                        quantity=related_book_order['book_order__quantity'],
                        publisher_package=package
                    ) for related_book_order in related_orders.values('book_order__book', 'book_order__quantity')
                ]
            )
            publisher_package_count += 1

        self.stdout.write(self.style.SUCCESS(f'{publisher_package_count} Publisher packages created.'))

        # ------------------------------------------------------------------
        # Create school packages
        # ------------------------------------------------------------------

        # Get unique schools in order
        school_ids = orders.values_list('created_by', flat=True).distinct('created_by')

        school_package_count = 0
        courier_package_count = 0

        # Create packages for each school
        for school_id in school_ids:
            school = User.objects.get(id=school_id)
            related_orders = orders.filter(created_by=school)
            school_package = SchoolPackage.objects.create(
                status=SchoolPackage.Status.PENDING.value, school=school
            )
            school_package.related_orders.set(related_orders)
            school_package_created = SchoolPackageBook.objects.bulk_create(
                [
                    SchoolPackageBook(
                        book_id=related_book_order['book_order__book'],
                        quantity=related_book_order['book_order__quantity'],
                        school_package=school_package
                    ) for related_book_order in related_orders.values('book_order__book', 'book_order__quantity')
                ]
            )
            school_package_count += 1

            # ------------------------------------------------------------------
            # Create courier packages
            # ------------------------------------------------------------------
            courier_package = CourierPackage.objects.create(status=SchoolPackage.Status.PENDING.value)
            courier_package.related_orders.set(related_orders)
            courier_package.school_package_books.set(school_package_created)
            courier_package_count += 1

        self.stdout.write(self.style.SUCCESS(f'{school_package_count} School packages created.'))
        self.stdout.write(self.style.SUCCESS(f'{courier_package_count} School courier created.'))
