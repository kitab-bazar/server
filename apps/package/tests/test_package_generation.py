from django.utils import timezone
from django.core.management import call_command

from utils.graphene.tests import GraphQLTestCase

from apps.user.models import User
from apps.order.models import Order

from apps.user.factories import UserFactory
from apps.book.factories import BookFactory
from apps.publisher.factories import PublisherFactory
from apps.order.factories import (
    BookOrderFactory,
    OrderFactory,
    OrderWindowFactory,
)
from apps.package.models import SchoolPackage, PublisherPackage, CourierPackage


class TestPackageGeneration(GraphQLTestCase):

    SCHOOL_PACKAGE_QUERY = '''
        query MyQuery {
          schoolPackages {
            results {
              status
              relatedOrders {
                totalPrice
                totalQuantity
              }
              schoolPackageBooks {
                results {
                  quantity
                }
              }
            }
          }
        }
    '''

    PUBLISHER_PACKAGE_QUERY = '''
        query MyQuery {
          publisherPackages {
            results {
              status
              publisherPackageBooks {
                results {
                  id
                  quantity
                }
              }
              relatedOrders {
                totalPrice
                totalQuantity
              }
            }
          }
        }
    '''

    COURIER_PACKAGE = '''
        query MyQuery {
          courierPackages {
            results {
              status
              courierPackageBooks {
                results {
                  quantity
                  id
                }
              }
              relatedOrders {
                totalPrice
                totalQuantity
              }
            }
          }
        }
    '''

    def setUp(self):
        self.user = UserFactory.create()
        self.p_1, self.p_2 = PublisherFactory.create_batch(2)
        self.u1_p1 = UserFactory.create(publisher=self.p_1, user_type=User.UserType.PUBLISHER)
        self.u2_p2 = UserFactory.create(publisher=self.p_2, user_type=User.UserType.PUBLISHER)
        self.moderator = UserFactory.create(user_type=User.UserType.MODERATOR)

        self.s_1, self.s_2 = UserFactory.create_batch(2, user_type=User.UserType.SCHOOL_ADMIN)

        # Create books
        self.p_1_b_1, self.p_1_b_2, self.p_1_b_3 = BookFactory.create_batch(3, publisher=self.p_1)
        self.p_2_b_1, self.p_2_b_2, self.p_2_b_3 = BookFactory.create_batch(3, publisher=self.p_2)

        order_window = OrderWindowFactory.create(
            start_date=timezone.now() - timezone.timedelta(5),
            end_date=timezone.now() + timezone.timedelta(5),
        )
        # Create orders for each school
        self.s_1_o_1, self.s_1_o_2, self.s_1_o_3 = OrderFactory.create_batch(
            3, created_by=self.s_1, status=Order.Status.PENDING, assigned_order_window=order_window
        )
        self.s_2_o_1, self.s_2_o_2 = OrderFactory.create_batch(
            2, created_by=self.s_2, status=Order.Status.PENDING, assigned_order_window=order_window
        )

        # Create book order for first school
        BookOrderFactory.create(order=self.s_1_o_1, book=self.p_1_b_1, quantity=30)
        BookOrderFactory.create(order=self.s_1_o_2, book=self.p_1_b_2, quantity=30)
        BookOrderFactory.create(order=self.s_1_o_3, book=self.p_1_b_3, quantity=30)

        # Create book order for second school
        BookOrderFactory.create(order=self.s_2_o_1, book=self.p_2_b_1, quantity=40)
        BookOrderFactory.create(order=self.s_2_o_2, book=self.p_2_b_2, quantity=40)

        # Generate packages
        call_command('generate_packages')

        super().setUp()

    def test_school_packages(self):

        # Test school 1
        self.force_login(self.s_1)
        content = self.query_check(self.SCHOOL_PACKAGE_QUERY)['data']
        self.assertEqual(content['schoolPackages']['results'][0]['status'], SchoolPackage.Status.PENDING.name)

        # Test should create only one package for one school
        self.assertEqual(len(content['schoolPackages']['results']), 1)

        # Test should create 3 related oorders and 3 school package books
        self.assertEqual(len(content['schoolPackages']['results'][0]['relatedOrders']), 3)
        self.assertEqual(len(content['schoolPackages']['results'][0]['schoolPackageBooks']['results']), 3)

        # Test school 2
        self.force_login(self.s_2)
        content = self.query_check(self.SCHOOL_PACKAGE_QUERY)['data']
        self.assertEqual(content['schoolPackages']['results'][0]['status'], SchoolPackage.Status.PENDING.name)

        # Test should create only one package for one school
        self.assertEqual(len(content['schoolPackages']['results']), 1)

        # Test should create 2 related oorders and 2 school package books
        self.assertEqual(len(content['schoolPackages']['results'][0]['relatedOrders']), 2)
        self.assertEqual(len(content['schoolPackages']['results'][0]['schoolPackageBooks']['results']), 2)

    def test_publisher_packages(self):

        # Test publisher 1
        self.force_login(self.u1_p1)
        content = self.query_check(self.PUBLISHER_PACKAGE_QUERY)['data']
        self.assertEqual(content['publisherPackages']['results'][0]['status'], PublisherPackage.Status.PENDING.name)

        # Test should create only one package for one publisher
        self.assertEqual(len(content['publisherPackages']['results']), 1)

        # Test should create 3 related oorders and 3 publisher package books
        self.assertEqual(len(content['publisherPackages']['results'][0]['relatedOrders']), 3)
        self.assertEqual(len(content['publisherPackages']['results'][0]['publisherPackageBooks']['results']), 3)

        # # Test publisher 2
        self.force_login(self.u2_p2)
        content = self.query_check(self.PUBLISHER_PACKAGE_QUERY)['data']
        self.assertEqual(content['publisherPackages']['results'][0]['status'], PublisherPackage.Status.PENDING.name)

        # Test should create only one package for one publisher
        self.assertEqual(len(content['publisherPackages']['results']), 1)

        # Test should create 2 related oorders and 2 publisher package books
        self.assertEqual(len(content['publisherPackages']['results'][0]['relatedOrders']), 2)
        self.assertEqual(len(content['publisherPackages']['results'][0]['publisherPackageBooks']['results']), 2)

    def test_courier_packages(self):

        # Test publisher 1
        self.force_login(self.moderator)
        content = self.query_check(self.COURIER_PACKAGE)['data']
        self.assertEqual(content['courierPackages']['results'][0]['status'], CourierPackage.Status.PENDING.name)

        # Test should list two schools packages
        self.assertEqual(len(content['courierPackages']['results']), 2)

        # Test should create 3 related oorders and 3 courier package books
        self.assertEqual(len(content['courierPackages']['results'][0]['relatedOrders']), 3)
        self.assertEqual(len(content['courierPackages']['results'][0]['courierPackageBooks']['results']), 3)
        self.assertEqual(len(content['courierPackages']['results'][1]['relatedOrders']), 2)
        self.assertEqual(len(content['courierPackages']['results'][1]['courierPackageBooks']['results']), 2)
