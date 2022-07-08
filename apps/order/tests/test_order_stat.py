from django.utils import timezone

from apps.common.tests.test_permissions import TestPermissions
from apps.user.models import User
from apps.order.models import Order
from apps.book.models import Book

from apps.user.factories import UserFactory
from apps.book.factories import BookFactory
from apps.publisher.factories import PublisherFactory
from apps.order.factories import OrderFactory, BookOrderFactory


class TestOrderState(TestPermissions):
    def setUp(self):
        super(TestOrderState, self).setUp()
        self.order_stat = '''
            query MyQuery {
              orderStat {
                ordersCompletedCount
                totalBooksOrdered
                totalBooksUploaded
                stat {
                  createdAtDate
                  totalQuantity
                }
              }
            }
        '''
        self.stat_to = timezone.now()
        stat_from = self.stat_to - timezone.timedelta(90)
        intermediate_date = self.stat_to - timezone.timedelta(15)
        not_in_range_date = self.stat_to - timezone.timedelta(120)

        # Create publishers
        self.publisher_1 = PublisherFactory.create()
        self.publisher_2 = PublisherFactory.create()

        # Create publisher users
        self.publisher_user_1 = UserFactory.create(
            user_type=User.UserType.PUBLISHER, publisher=self.publisher_1
        )
        self.publisher_user_2 = UserFactory.create(
            user_type=User.UserType.PUBLISHER, publisher=self.publisher_2
        )

        # Create 4 book in different date range
        self.book_1 = BookFactory.create(publisher=self.publisher_1, published_date=self.stat_to)
        self.book_2 = BookFactory.create(publisher=self.publisher_1, published_date=stat_from)
        self.book_3 = BookFactory.create(publisher=self.publisher_2, published_date=intermediate_date)
        self.book_4 = BookFactory.create(publisher=self.publisher_2, published_date=not_in_range_date)

        # Create 3 book orders
        order_1 = OrderFactory.create(
            created_by=self.individual_user, status=Order.Status.COMPLETED, created_at=self.stat_to
        )
        order_2 = OrderFactory.create(
            created_by=self.individual_user, status=Order.Status.COMPLETED, created_at=self.stat_to
        )
        order_3 = OrderFactory.create(
            created_by=self.individual_user, status=Order.Status.COMPLETED, created_at=self.stat_to
        )

        # Create 4 book orders each having 5 quantity and 500 price
        BookOrderFactory.create(
            order=order_1, book=self.book_1, quantity=5,
            grade=Book.Grade.GRADE_1.value, language=Book.LanguageType.ENGLISH.value
        )
        BookOrderFactory.create(
            order=order_2, book=self.book_2, quantity=5,
            grade=Book.Grade.GRADE_1.value, language=Book.LanguageType.ENGLISH.value
        )
        BookOrderFactory.create(
            order=order_3, book=self.book_3, quantity=5,
            grade=Book.Grade.GRADE_1.value, language=Book.LanguageType.ENGLISH.value
        )
        super().setUp()

    def test_admin_can_see_overall_stat(self):
        self.force_login(self.super_admin)
        content = self.query_check(self.order_stat)
        order_stat = content['data']['orderStat']
        # Test shoudl retrive correct count
        self.assertEqual(order_stat['totalBooksOrdered'], 15)
        self.assertEqual(order_stat['totalBooksUploaded'], 4)
        self.assertEqual(order_stat['ordersCompletedCount'], 3)

        # Test shoudl retrive quantity count
        self.assertEqual(order_stat['stat'][0]['createdAtDate'], str(self.stat_to.date()))
        self.assertEqual(order_stat['stat'][0]['totalQuantity'], 15)

    def test_publisher_can_see_their_stat_only(self):
        # ------------------------------------
        # Test for first publisher
        # ------------------------------------
        self.force_login(self.publisher_user_1)
        content = self.query_check(self.order_stat)
        order_stat = content['data']['orderStat']
        # Test shoudl retrive correct count
        self.assertEqual(order_stat['totalBooksOrdered'], 10)
        self.assertEqual(order_stat['totalBooksUploaded'], 2)
        self.assertEqual(order_stat['ordersCompletedCount'], 2)

        # Test shoudl retrive quantity count
        self.assertEqual(order_stat['stat'][0]['createdAtDate'], str(self.stat_to.date()))
        self.assertEqual(order_stat['stat'][0]['totalQuantity'], 10)

        # ------------------------------------
        # Test second first publisher
        # ------------------------------------
        self.force_login(self.publisher_user_1)
        content = self.query_check(self.order_stat)
        order_stat = content['data']['orderStat']
        self.assertEqual(order_stat['totalBooksOrdered'], 10)
        self.assertEqual(order_stat['totalBooksUploaded'], 2)
        self.assertEqual(order_stat['ordersCompletedCount'], 2)
        self.assertEqual(order_stat['stat'][0]['createdAtDate'], str(self.stat_to.date()))
        self.assertEqual(order_stat['stat'][0]['totalQuantity'], 10)

    def test_school_admin_can_see_their_stat_only(self):
        order = OrderFactory.create(created_by=self.school_admin_user, status=Order.Status.COMPLETED)
        BookOrderFactory.create(
            order=order, book=self.book_1, quantity=10,
            grade=Book.Grade.GRADE_1.value, language=Book.LanguageType.ENGLISH.value
        )
        self.force_login(self.school_admin_user)
        content = self.query_check(self.order_stat)
        order_stat = content['data']['orderStat']
        self.assertEqual(order_stat['stat'][0]['createdAtDate'], str(self.stat_to.date()))
        self.assertEqual(order_stat['stat'][0]['totalQuantity'], 10)

    def test_individual_user_can_see_their_stat_only(self):
        order = OrderFactory.create(created_by=self.individual_user, status=Order.Status.COMPLETED)
        BookOrderFactory.create(
            order=order, book=self.book_1, quantity=30,
            grade=Book.Grade.GRADE_1.value, language=Book.LanguageType.ENGLISH.value
        )
        self.force_login(self.individual_user)
        content = self.query_check(self.order_stat)
        order_stat = content['data']['orderStat']
        self.assertEqual(order_stat['stat'][0]['createdAtDate'], str(self.stat_to.date()))
        self.assertEqual(order_stat['stat'][0]['totalQuantity'], 30)
