from django.core.management.base import BaseCommand
from django.db.models import Sum, F, Q
from django.db import IntegrityError

from apps.publisher.models import Publisher
from apps.order.models import Order, OrderWindow, BookOrder
from apps.package.models import PublisherPackage, PublisherPackageBook, SchoolPackage, SchoolPackageBook, CourierPackage
from apps.user.models import User
from apps.common.models import Municipality


class Command(BaseCommand):
    help = 'Generate publisher packages'

    def add_arguments(self, parser):
        parser.add_argument('order_window_id', type=int, help='order window id')

    def _generate_packages(self, latest_order_window, orders):
        # ------------------------------------------------------------------
        # Create publihser packages
        # ------------------------------------------------------------------

        # Get unique publishers in order
        publisher_ids = orders.values_list('book_order__publisher', flat=True).distinct()

        publisher_package_count = 0

        # Create packages for each publishers
        for publisher_id in publisher_ids:
            publisher = Publisher.objects.get(id=publisher_id)
            related_orders = orders.filter(book_order__publisher=publisher)
            related_book_orders = BookOrder.objects.filter(order__in=related_orders).values('book').annotate(
                total_quantity=Sum('quantity'),
                total_price=Sum('quantity') * F('price')
            ).values('book', 'total_quantity', 'total_price')
            package = PublisherPackage.objects.create(
                status=PublisherPackage.Status.PENDING.value,
                publisher=publisher,
                order_window=latest_order_window,
                total_quantity=related_book_orders.aggregate(
                    grand_total_quantity=Sum('total_quantity'))['grand_total_quantity'],
                total_price=related_book_orders.aggregate(
                    grand_total_price=Sum('total_price'))['grand_total_price']
            )
            package.related_orders.set(related_orders)
            PublisherPackageBook.objects.bulk_create(
                [
                    PublisherPackageBook(
                        book_id=related_book_order['book'],
                        quantity=related_book_order['total_quantity'],
                        publisher_package=package
                    ) for related_book_order in related_book_orders
                ]
            )
            publisher_package_count += 1

        self.stdout.write(self.style.SUCCESS(f'{publisher_package_count} Publisher packages created.'))

        # ------------------------------------------------------------------
        # Create courier packages
        # ------------------------------------------------------------------
        courier_package_count = 0
        municipality_ids = orders.values_list(
            'created_by__school__municipality', flat=True
        ).distinct()
        for municipality_id in municipality_ids:
            courier_related_book_orders = orders.filter(
                created_by__school__municipality=municipality_id
            ).values(
                'created_by__school__municipality'
            ).annotate(
                total_quantity=Sum('book_order__quantity'),
                total_price=Sum('book_order__quantity') * F('book_order__price')
            ).values('total_quantity', 'total_price')

            CourierPackage.objects.create(
                status=CourierPackage.Status.PENDING.value,
                order_window=latest_order_window,
                municipality=Municipality.objects.get(id=municipality_id),
                total_quantity=courier_related_book_orders.aggregate(
                    grand_total_quantity=Sum('total_quantity'))['grand_total_quantity'],
                total_price=courier_related_book_orders.aggregate(
                    grand_total_price=Sum('total_price'))['grand_total_price']
            )
            courier_package_count += 1
        self.stdout.write(self.style.SUCCESS(f'{courier_package_count} municipality/courier packages created.'))

        # ------------------------------------------------------------------
        # Create school packages
        # ------------------------------------------------------------------

        # Get unique schools in order
        school_ids = orders.values_list('created_by', flat=True).distinct('created_by')
        school_package_count = 0

        # Create packages for each school
        for school_id in school_ids:
            school = User.objects.get(id=school_id)
            related_orders = orders.filter(created_by=school)
            related_book_orders = BookOrder.objects.filter(order__in=related_orders).values('book__created_by').annotate(
                total_quantity=Sum('quantity'),
                total_price=Sum('quantity') * F('price')
            ).values('book', 'total_quantity', 'total_price')
            courier_package = CourierPackage.objects.get(
                order_window=latest_order_window, municipality=school.school.municipality
            )
            school_package = SchoolPackage.objects.create(
                status=SchoolPackage.Status.PENDING.value,
                school=school,
                order_window=latest_order_window,
                courier_package=courier_package,
                total_quantity=related_book_orders.aggregate(
                    grand_total_quantity=Sum('total_quantity'))['grand_total_quantity'],
                total_price=related_book_orders.aggregate(
                    grand_total_price=Sum('total_price'))['grand_total_price']
            )
            school_package.related_orders.set(related_orders)
            SchoolPackageBook.objects.bulk_create(
                [
                    SchoolPackageBook(
                        book_id=related_book_order['book'],
                        quantity=related_book_order['total_quantity'],
                        school_package=school_package,
                    ) for related_book_order in related_book_orders
                ]
            )
            school_package_count += 1

        self.stdout.write(self.style.SUCCESS(f'{school_package_count} School packages created.'))

    def _format_unverified_users(self, unverified_user_qs):
        return '\n'.join(
            ['id = %s ---- full name = %s' % (user['id'], user['created_by__full_name']) for user in unverified_user_qs]
        )

    def _format_unverified_payments(self, unverified_payments_qs):
        return '\n'.join(
            ['id = %s ---- full name = %s' % (user['id'], user['paid_by__full_name']) for user in unverified_payments_qs]
        )

    def handle(self, *args, **options):

        order_window_id = options['order_window_id']
        # Check if order window exists
        try:
            latest_order_window = OrderWindow.objects.get(id=order_window_id)
        except OrderWindow.DoesNotExist:
            self.stdout.write(self.style.ERROR('Invalid order window id supplied.'))
            return

        # Get orders belongs to order window
        orders = Order.objects.filter(
            book_order__publisher__isnull=False,
            assigned_order_window__id=latest_order_window.id,
            status=Order.Status.PENDING.value
        )
        user_ids = orders.values_list('created_by__id', flat=True)
        if User.objects.filter(id__in=user_ids).annotate(**User.annotate_mismatch_order_statements()).filter(
            outstanding_balance__lt=0
        ).exists():
            self.stdout.write(self.style.ERROR(
                'Mismatched orders exists please fix those'
            ))
            return

        # Check if unverified users exists
        unverified_users_qs = orders.filter(
            Q(created_by__is_verified=False) | Q(created_by__school__isnull=True) | Q(created_by__is_deactivated=True)
        ).distinct()
        if unverified_users_qs.exists():
            unverified_users = unverified_users_qs.values('id', 'created_by__full_name')
            formated_unverified_users = self._format_unverified_users(unverified_users)
            self.stdout.write(self.style.ERROR(
                'Following users are not verified or school profile is not attached \n'
                f'{formated_unverified_users}'
            ))
            return

        # Check if packages are already created
        if (
            PublisherPackage.objects.filter(order_window=latest_order_window).exists() or
            PublisherPackage.objects.filter(order_window=latest_order_window).exists() or
            PublisherPackage.objects.filter(order_window=latest_order_window).exists()
        ):
            f'Packages for order window {latest_order_window} are already created.'

        try:
            self._generate_packages(latest_order_window, orders)
        except IntegrityError:
            self.stdout.write(self.style.ERROR(
                f'Packages for order window {latest_order_window} are already created.'
            ))
            return
