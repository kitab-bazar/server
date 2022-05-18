from openpyxl.workbook import Workbook
import os

from django.db import transaction
from django.db.models import Sum
from django.core.management.base import BaseCommand
from apps.order.models import OrderWindow
from apps.package.models import SchoolPackage
from apps.package.seed.incentive import INCENTIVE_BOOKS


class Command(BaseCommand):
    help = 'Delete package of particular order window'

    def add_arguments(self, parser):
        parser.add_argument('order_window_id', type=int, help='order window id')

    @transaction.atomic
    def handle(self, *args, **options):
        order_window_id = options['order_window_id']
        # Check if order window exists
        try:
            order_window = OrderWindow.objects.get(id=order_window_id)
        except OrderWindow.DoesNotExist:
            self.stdout.write(self.style.ERROR('Invalid order window id supplied.'))
            return

        school_packages = SchoolPackage.objects.filter(order_window=order_window)

        wb = Workbook()

        for package in school_packages:
            row = 1
            sheet = wb.create_sheet(f'{package.school.school} - {package.school.school.municipality}')
            school_detail = f'{package.school.school} / {package.school.school.district} / {package.school.school.municipality}' # noqa
            sheet.append([school_detail])
            sheet.append([])
            sheet.append(['Book Name', 'Publisher Name', 'Quantity', 'Price', 'Sub Total', 'Total'])

            for order in package.related_orders.all():
                total_book_order_price = 0
                total_book_order_quantity = 0
                for book_order in order.book_order.all():
                    sub_total = book_order.quantity * book_order.price
                    sheet.append([
                        book_order.title,
                        book_order.publisher.name,
                        book_order.quantity,
                        book_order.price,
                        sub_total,
                        book_order.total_price
                    ])
                    row += 1
                    total_book_order_price += sub_total
                    total_book_order_quantity += book_order.quantity

                sheet.append([])
                sheet.append(['', '', 'Total Quantity', total_book_order_quantity, 'Total Price', total_book_order_price])
                sheet.append([])
                sheet.append([])
                sheet.append([])
                incentive_detail = f'{package.school.school} / {package.school.school.district} / {package.school.school.municipality} Incentive books' # noqa
                sheet.append([incentive_detail])
                sheet.append([])

                sheet.append(['Book Name', 'Publisher Name', 'Quantity', 'Price', 'Sub Total'])
                incentive = order.book_order.all().aggregate(total_quantity=Sum('quantity'))['total_quantity']
                if incentive >= 10:
                    total_incentive_price = 0
                    total_incentive_quantity = 0
                    incentive_key = f'book_list_{incentive * 4}'
                    for book in INCENTIVE_BOOKS[incentive_key]:
                        sheet.append([
                            book['book_name'],
                            book['publisher_name'],
                            book['quantity'],
                            book['price'],
                            book['quantity'] * book['price']
                        ])
                        total_incentive_price += book['quantity'] * book['price']
                        total_incentive_quantity += book['quantity']
                sheet.append([])
                sheet.append(['', 'Total Quantity', total_incentive_quantity, 'Total Price', total_incentive_price])

        # Make sure generated directory exists
        try:
            os.makedirs("generated")
        except FileExistsError:
            pass
        wb.save(filename="generated/school_bill.xlsx")
