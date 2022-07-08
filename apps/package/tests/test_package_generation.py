from django.utils import timezone
from django.core.management import call_command

from utils.graphene.tests import GraphQLTestCase

from apps.user.models import User
from apps.order.models import Order, OrderWindow
from apps.payment.models import Payment

from apps.user.factories import UserFactory
from apps.book.factories import BookFactory
from apps.publisher.factories import PublisherFactory
from apps.order.factories import (
    BookOrderFactory,
    OrderFactory,
    OrderWindowFactory,
)
from apps.package.models import (
    SchoolPackage, PublisherPackage, CourierPackage, InstitutionPackage
)
from apps.school.factories import SchoolFactory
from apps.institution.factories import InstitutionFactory
from apps.common.factories import MunicipalityFactory
from apps.payment.factories import PaymentFactory


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
              totalPrice
              totalQuantity
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
              totalPrice
              totalQuantity
            }
          }
        }
    '''

    SCHOOL_COURIER_PACKAGE_QUERY = '''
        query MyQuery {
          courierPackages {
            results {
              status
              schoolCourierPackageBooks {
                results {
                  quantity
                  id
                }
              }
              relatedOrders {
                totalPrice
                totalQuantity
              }
              municipality {
                id
              }
              totalPrice
              totalQuantity
            }
          }
        }
    '''

    INSTITUTION_PACKAGE_QUERY = '''
        query MyQuery {
          institutionPackages {
            results {
              status
              relatedOrders {
                totalPrice
                totalQuantity
              }
              institutionPackageBooks {
                results {
                  quantity
                }
              }
              totalPrice
              totalQuantity
            }
          }
        }
    '''

    INSTITUTION_COURIER_PACKAGE_QUERY = '''
        query MyQuery {
          courierPackages {
            results {
              status
              institutionCourierPackageBooks {
                results {
                  quantity
                  id
                }
              }
              relatedOrders {
                totalPrice
                totalQuantity
              }
              municipality {
                id
              }
              totalPrice
              totalQuantity
            }
          }
        }
    '''

    def setUp(self):
        self.p_1, self.p_2 = PublisherFactory.create_batch(2)
        self.u1_p1 = UserFactory.create(publisher=self.p_1, user_type=User.UserType.PUBLISHER, is_verified=True)
        self.u2_p2 = UserFactory.create(publisher=self.p_2, user_type=User.UserType.PUBLISHER, is_verified=True)
        self.moderator = UserFactory.create(user_type=User.UserType.MODERATOR, is_verified=True)

        m1, m2, m3, m4 = MunicipalityFactory.create_batch(4)

        self.s_1 = UserFactory.create(
            user_type=User.UserType.SCHOOL_ADMIN, is_verified=True, school=SchoolFactory.create(municipality=m1)
        )
        self.s_2 = UserFactory.create(
            user_type=User.UserType.SCHOOL_ADMIN, is_verified=True, school=SchoolFactory.create(municipality=m2)
        )
        self.i_1 = UserFactory.create(
            user_type=User.UserType.INSTITUTIONAL_USER, is_verified=True,
            institution=InstitutionFactory.create(municipality=m3)
        )
        self.i_2 = UserFactory.create(
            user_type=User.UserType.INSTITUTIONAL_USER, is_verified=True,
            institution=InstitutionFactory.create(municipality=m4)
        )

        # Create books
        self.p_1_b_1, self.p_1_b_2, self.p_1_b_3 = BookFactory.create_batch(3, publisher=self.p_1, price=100)
        self.p_2_b_1, self.p_2_b_2, self.p_2_b_3 = BookFactory.create_batch(3, publisher=self.p_2, price=100)

        self.school_order_window = OrderWindowFactory.create(
            start_date=timezone.now() - timezone.timedelta(5),
            end_date=timezone.now() + timezone.timedelta(5),
            type=OrderWindow.OrderWindowType.SCHOOL
        )
        self.institution_order_window = OrderWindowFactory.create(
            start_date=timezone.now() - timezone.timedelta(5),
            end_date=timezone.now() + timezone.timedelta(5),
            type=OrderWindow.OrderWindowType.INSTITUTION
        )
        # Create orders for each school
        self.s_1_o_1, self.s_1_o_2, self.s_1_o_3 = OrderFactory.create_batch(
            3, created_by=self.s_1, status=Order.Status.PENDING, assigned_order_window=self.school_order_window
        )
        self.s_2_o_1, self.s_2_o_2 = OrderFactory.create_batch(
            2, created_by=self.s_2, status=Order.Status.PENDING, assigned_order_window=self.school_order_window
        )
        self.i_1_o_1, self.i_1_o_2, self.i_1_o_3, self.i_1_o_4 = OrderFactory.create_batch(
            4, created_by=self.i_1, status=Order.Status.PENDING,
            assigned_order_window=self.institution_order_window
        )
        self.i_2_o_1, self.i_2_o_2, self.i_2_o_3, self.i_2_o_4 = OrderFactory.create_batch(
            4, created_by=self.i_2, status=Order.Status.PENDING,
            assigned_order_window=self.institution_order_window
        )

        # Create book order for first school
        BookOrderFactory.create(order=self.s_1_o_1, book=self.p_1_b_1, quantity=30)
        BookOrderFactory.create(order=self.s_1_o_2, book=self.p_1_b_2, quantity=30)
        BookOrderFactory.create(order=self.s_1_o_3, book=self.p_1_b_3, quantity=30)

        # Create book order for second school
        BookOrderFactory.create(order=self.s_2_o_1, book=self.p_2_b_1, quantity=40)
        BookOrderFactory.create(order=self.s_2_o_2, book=self.p_2_b_2, quantity=40)

        # Create book order for first institution
        BookOrderFactory.create(order=self.i_1_o_1, book=self.p_1_b_1, quantity=10)
        BookOrderFactory.create(order=self.i_1_o_2, book=self.p_2_b_2, quantity=10)
        BookOrderFactory.create(order=self.i_1_o_3, book=self.p_2_b_3, quantity=10)
        BookOrderFactory.create(order=self.i_1_o_4, book=self.p_2_b_1, quantity=10)

        # Create book order for second institution
        BookOrderFactory.create(order=self.i_2_o_1, book=self.p_1_b_1, quantity=10)
        BookOrderFactory.create(order=self.i_2_o_2, book=self.p_2_b_2, quantity=10)
        BookOrderFactory.create(order=self.i_2_o_3, book=self.p_2_b_3, quantity=10)
        BookOrderFactory.create(order=self.i_2_o_4, book=self.p_2_b_1, quantity=10)

        # Create payment for each schools and institutions
        for school in [self.s_1, self.s_2, self.i_1, self.i_2]:
            PaymentFactory.create(
                created_by=self.moderator,
                modified_by=self.moderator,
                paid_by=school,
                amount=30000,
                transaction_type=Payment.TransactionType.CREDIT,
                payment_type=Payment.PaymentType.CASH,
                status=Payment.Status.VERIFIED.value
            )

        super().setUp()

    def test_school_packages(self):
        call_command('generate_packages', self.school_order_window.id)

        # Test school 1
        self.force_login(self.s_1)
        content = self.query_check(self.SCHOOL_PACKAGE_QUERY)['data']
        self.assertEqual(content['schoolPackages']['results'][0]['status'], SchoolPackage.Status.PENDING.name)

        # Test should create only one package for one school
        self.assertEqual(len(content['schoolPackages']['results']), 1)

        # Test should create 3 related oorders and 3 school package books
        self.assertEqual(len(content['schoolPackages']['results'][0]['relatedOrders']), 3)
        self.assertEqual(len(content['schoolPackages']['results'][0]['schoolPackageBooks']['results']), 3)
        self.assertEqual(content['schoolPackages']['results'][0]['totalPrice'], 9000)
        self.assertEqual(content['schoolPackages']['results'][0]['totalQuantity'], 90)

        # Test school 2
        self.force_login(self.s_2)
        content = self.query_check(self.SCHOOL_PACKAGE_QUERY)['data']
        self.assertEqual(content['schoolPackages']['results'][0]['status'], SchoolPackage.Status.PENDING.name)

        # Test should create only one package for one school
        self.assertEqual(len(content['schoolPackages']['results']), 1)

        # Test should create 2 related oorders and 2 school package books
        self.assertEqual(len(content['schoolPackages']['results'][0]['relatedOrders']), 2)
        self.assertEqual(len(content['schoolPackages']['results'][0]['schoolPackageBooks']['results']), 2)
        self.assertEqual(content['schoolPackages']['results'][0]['totalPrice'], 8000)
        self.assertEqual(content['schoolPackages']['results'][0]['totalQuantity'], 80)

    def test_publisher_packages(self):
        call_command('generate_packages', self.school_order_window.id)

        # Test publisher 1
        self.force_login(self.u1_p1)
        content = self.query_check(self.PUBLISHER_PACKAGE_QUERY)['data']
        self.assertEqual(content['publisherPackages']['results'][0]['status'], PublisherPackage.Status.PENDING.name)

        # Test should create only one package for one publisher
        self.assertEqual(len(content['publisherPackages']['results']), 1)

        # Test should create 3 related oorders and 3 publisher package books
        self.assertEqual(len(content['publisherPackages']['results'][0]['relatedOrders']), 3)
        self.assertEqual(len(content['publisherPackages']['results'][0]['publisherPackageBooks']['results']), 3)
        self.assertEqual(content['publisherPackages']['results'][0]['totalPrice'], 9000)
        self.assertEqual(content['publisherPackages']['results'][0]['totalQuantity'], 90)

        # # Test publisher 2
        self.force_login(self.u2_p2)
        content = self.query_check(self.PUBLISHER_PACKAGE_QUERY)['data']
        self.assertEqual(content['publisherPackages']['results'][0]['status'], PublisherPackage.Status.PENDING.name)

        # Test should create only one package for one publisher
        self.assertEqual(len(content['publisherPackages']['results']), 1)

        # Test should create 2 related oorders and 2 publisher package books
        self.assertEqual(len(content['publisherPackages']['results'][0]['relatedOrders']), 2)
        self.assertEqual(len(content['publisherPackages']['results'][0]['publisherPackageBooks']['results']), 2)
        self.assertEqual(content['publisherPackages']['results'][0]['totalPrice'], 8000)
        self.assertEqual(content['publisherPackages']['results'][0]['totalQuantity'], 80)

    def test_courier_packages(self):
        call_command('generate_packages', self.school_order_window.id)
        # Test publisher 1
        self.force_login(self.moderator)
        content = self.query_check(self.SCHOOL_COURIER_PACKAGE_QUERY)['data']
        self.assertEqual(content['courierPackages']['results'][0]['status'], CourierPackage.Status.PENDING.name)

        # Test should list two schools packages
        self.assertEqual(len(content['courierPackages']['results']), 2)

        # Test should create 3 related oorders and 3 courier package books
        self.assertEqual(len(content['courierPackages']['results'][0]['relatedOrders']), 3)
        self.assertEqual(len(content['courierPackages']['results'][0]['schoolCourierPackageBooks']['results']), 3)
        self.assertEqual(len(content['courierPackages']['results'][1]['relatedOrders']), 2)
        self.assertEqual(len(content['courierPackages']['results'][1]['schoolCourierPackageBooks']['results']), 2)
        self.assertEqual(content['courierPackages']['results'][0]['totalPrice'], 9000)
        self.assertEqual(content['courierPackages']['results'][0]['totalQuantity'], 90)

        self.assertEqual(content['courierPackages']['results'][1]['totalPrice'], 8000)
        self.assertEqual(content['courierPackages']['results'][1]['totalQuantity'], 80)

    def test_institution_packages(self):
        call_command('generate_packages', self.institution_order_window.id)

        # Test school 1
        self.force_login(self.i_1)
        content = self.query_check(self.INSTITUTION_PACKAGE_QUERY)['data']
        self.assertEqual(content['institutionPackages']['results'][0]['status'], InstitutionPackage.Status.PENDING.name)

        # Test should create only one package for one school
        self.assertEqual(len(content['institutionPackages']['results']), 1)

        # Test should create 3 related oorders and 3 school package books
        self.assertEqual(len(content['institutionPackages']['results'][0]['relatedOrders']), 4)
        self.assertEqual(len(content['institutionPackages']['results'][0]['institutionPackageBooks']['results']), 4)
        self.assertEqual(content['institutionPackages']['results'][0]['totalPrice'], 4000)
        self.assertEqual(content['institutionPackages']['results'][0]['totalQuantity'], 40)

        # Test school 2
        self.force_login(self.i_2)
        content = self.query_check(self.INSTITUTION_PACKAGE_QUERY)['data']
        self.assertEqual(content['institutionPackages']['results'][0]['status'], InstitutionPackage.Status.PENDING.name)

        # Test should create only one package for one school
        self.assertEqual(len(content['institutionPackages']['results']), 1)

        # Test should create 2 related oorders and 2 school package books
        self.assertEqual(len(content['institutionPackages']['results'][0]['relatedOrders']), 4)
        self.assertEqual(len(content['institutionPackages']['results'][0]['institutionPackageBooks']['results']), 4)
        self.assertEqual(content['institutionPackages']['results'][0]['totalPrice'], 4000)
        self.assertEqual(content['institutionPackages']['results'][0]['totalQuantity'], 40)

    def test_institution_publisher_packages(self):
        call_command('generate_packages', self.institution_order_window.id)

        # Test publisher 1
        self.force_login(self.u1_p1)
        content = self.query_check(self.PUBLISHER_PACKAGE_QUERY)['data']
        self.assertEqual(content['publisherPackages']['results'][0]['status'], PublisherPackage.Status.PENDING.name)
        self.assertEqual(len(content['publisherPackages']['results']), 1)
        self.assertEqual(len(content['publisherPackages']['results'][0]['relatedOrders']), 2)
        self.assertEqual(len(content['publisherPackages']['results'][0]['publisherPackageBooks']['results']), 1)
        self.assertEqual(content['publisherPackages']['results'][0]['totalPrice'], 2000)
        self.assertEqual(content['publisherPackages']['results'][0]['totalQuantity'], 20)

        # # Test publisher 2
        self.force_login(self.u2_p2)
        content = self.query_check(self.PUBLISHER_PACKAGE_QUERY)['data']
        self.assertEqual(content['publisherPackages']['results'][0]['status'], PublisherPackage.Status.PENDING.name)

        self.assertEqual(len(content['publisherPackages']['results']), 1)
        self.assertEqual(len(content['publisherPackages']['results'][0]['relatedOrders']), 6)
        self.assertEqual(len(content['publisherPackages']['results'][0]['publisherPackageBooks']['results']), 3)
        self.assertEqual(content['publisherPackages']['results'][0]['totalPrice'], 6000)
        self.assertEqual(content['publisherPackages']['results'][0]['totalQuantity'], 60)

    def test_institution_courier_packages(self):
        call_command('generate_packages', self.institution_order_window.id)
        self.force_login(self.moderator)
        content = self.query_check(self.INSTITUTION_COURIER_PACKAGE_QUERY)['data']
        self.assertEqual(content['courierPackages']['results'][0]['status'], CourierPackage.Status.PENDING.name)

        # Test should list two institution packages
        self.assertEqual(len(content['courierPackages']['results']), 2)

        # Test should create 4 related oorders and 8 courier package books
        self.assertEqual(len(content['courierPackages']['results'][0]['relatedOrders']), 4)
        self.assertEqual(len(content['courierPackages']['results'][0]['institutionCourierPackageBooks']['results']), 8)
        self.assertEqual(len(content['courierPackages']['results'][1]['relatedOrders']), 4)
        self.assertEqual(len(content['courierPackages']['results'][1]['institutionCourierPackageBooks']['results']), 8)
        self.assertEqual(content['courierPackages']['results'][0]['totalPrice'], 4000)
        self.assertEqual(content['courierPackages']['results'][0]['totalQuantity'], 40)
        self.assertEqual(content['courierPackages']['results'][1]['totalPrice'], 4000)
        self.assertEqual(content['courierPackages']['results'][1]['totalQuantity'], 40)
