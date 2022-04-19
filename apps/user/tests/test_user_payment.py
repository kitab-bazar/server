from utils.graphene.tests import GraphQLTestCase
from apps.user.models import User
from apps.payment.models import Payment
from apps.user.factories import UserFactory
from apps.order.models import Order
from apps.book.models import Book
from apps.payment.factories import PaymentFactory
from apps.order.factories import OrderFactory, BookOrderFactory
from apps.publisher.factories import PublisherFactory
from apps.book.factories import BookFactory


class UserPaymentTest(GraphQLTestCase):
    PAYMENT_QUERY = '''
        query MyQuery {
          moderatorQuery {
            users(userType: SCHOOL_ADMIN) {
              results {
                id
                outstandingBalance
                paymentCreditSum
                paymentDebitSum
                totalOrderPendingPrice
                totalUnverifiedPayment
                totalUnverifiedPaymentCount
                totalVerifiedPayment
                totalVerifiedPaymentCount
              }
            }
          }
        }
    '''

    PAYMENT_SUMMARY = '''
    query MyQuery {
      schoolQuery {
        paymentSummary {
          outstandingBalance
          paymentCreditSum
          paymentDebitSum
          totalUnverifiedPayment
          totalUnverifiedPaymentCount
          totalVerifiedPayment
          totalVerifiedPaymentCount
        }
      }
    }
    '''

    def setUp(self):
        self.school_1 = UserFactory.create(first_name='', last_name='', user_type=User.UserType.SCHOOL_ADMIN)
        self.moderator = UserFactory.create(first_name='', last_name='', user_type=User.UserType.MODERATOR)

    def test_initial_payment_fields(self):
        self.force_login(self.moderator)
        content = self.query_check(self.PAYMENT_QUERY)['data']
        self.assertEqual(content['moderatorQuery']['users']['results'][0]['id'], str(self.school_1.id))
        self.assertEqual(content['moderatorQuery']['users']['results'][0]['outstandingBalance'], 0)
        self.assertEqual(content['moderatorQuery']['users']['results'][0]['paymentCreditSum'], 0)
        self.assertEqual(content['moderatorQuery']['users']['results'][0]['paymentDebitSum'], 0)
        self.assertEqual(content['moderatorQuery']['users']['results'][0]['totalOrderPendingPrice'], 0)
        self.assertEqual(content['moderatorQuery']['users']['results'][0]['totalUnverifiedPayment'], 0)
        self.assertEqual(content['moderatorQuery']['users']['results'][0]['totalUnverifiedPaymentCount'], 0)
        self.assertEqual(content['moderatorQuery']['users']['results'][0]['totalVerifiedPayment'], 0)
        self.assertEqual(content['moderatorQuery']['users']['results'][0]['totalVerifiedPaymentCount'], 0)

    def _create_orders_for_user(self, user):
        publisher = PublisherFactory.create()
        book1 = BookFactory.create(publisher=publisher, price=100)
        book2 = BookFactory.create(publisher=publisher, price=200)
        book3 = BookFactory.create(publisher=publisher, price=300)

        # Create orders
        order_1 = OrderFactory.create(created_by=user, status=Order.Status.PENDING)
        order_2 = OrderFactory.create(created_by=user, status=Order.Status.PENDING)
        order_3 = OrderFactory.create(created_by=user, status=Order.Status.PENDING)

        BookOrderFactory.create(
            order=order_1, book=book1, quantity=10, grade=Book.Grade.GRADE_1.value, language=Book.LanguageType.ENGLISH.value
        )
        BookOrderFactory.create(
            order=order_2, book=book2, quantity=20, grade=Book.Grade.GRADE_1.value, language=Book.LanguageType.ENGLISH.value
        )
        BookOrderFactory.create(
            order=order_3, book=book3, quantity=30, grade=Book.Grade.GRADE_1.value, language=Book.LanguageType.ENGLISH.value
        )

    def test_debit_credit_and_order_for_school(self):
        self._create_orders_for_user(self.school_1)
        PaymentFactory.create_batch(
            2,
            created_by=self.moderator, modified_by=self.moderator,
            paid_by=self.school_1, amount=20000,
            transaction_type=Payment.TransactionType.CREDIT,
            status=Payment.Status.VERIFIED, payment_type=Payment.PaymentType.CASH
        )
        PaymentFactory.create_batch(
            2,
            created_by=self.moderator, modified_by=self.moderator,
            paid_by=self.school_1, amount=10000,
            transaction_type=Payment.TransactionType.DEBIT,
            status=Payment.Status.VERIFIED, payment_type=Payment.PaymentType.CASH
        )
        PaymentFactory.create_batch(
            2,
            created_by=self.moderator, modified_by=self.moderator,
            paid_by=self.school_1, amount=30000,
            transaction_type=Payment.TransactionType.CREDIT,
            status=Payment.Status.PENDING, payment_type=Payment.PaymentType.CASH
        )
        PaymentFactory.create_batch(
            2,
            created_by=self.moderator, modified_by=self.moderator,
            paid_by=self.school_1, amount=30000,
            transaction_type=Payment.TransactionType.CREDIT,
            status=Payment.Status.PENDING, payment_type=Payment.PaymentType.CASH
        )
        self.force_login(self.moderator)
        content = self.query_check(self.PAYMENT_QUERY)['data']
        self.assertEqual(content['moderatorQuery']['users']['results'][0]['id'], str(self.school_1.id))
        self.assertEqual(
            content['moderatorQuery']['users']['results'][0]['totalOrderPendingPrice'],
            100 * 10 + 200 * 20 + 300 * 30
        )
        self.assertEqual(
            content['moderatorQuery']['users']['results'][0]['outstandingBalance'],
            20000 - (100 * 10 + 200 * 20 + 300 * 30)
        )
        self.assertEqual(content['moderatorQuery']['users']['results'][0]['paymentCreditSum'], 40000)
        self.assertEqual(content['moderatorQuery']['users']['results'][0]['paymentDebitSum'], 20000)

        self.assertEqual(content['moderatorQuery']['users']['results'][0]['totalUnverifiedPayment'], 120000)
        self.assertEqual(content['moderatorQuery']['users']['results'][0]['totalUnverifiedPaymentCount'], 4)
        self.assertEqual(content['moderatorQuery']['users']['results'][0]['totalVerifiedPayment'], 40000)
        self.assertEqual(content['moderatorQuery']['users']['results'][0]['totalVerifiedPaymentCount'], 2)

        self.force_login(self.school_1)
        content = self.query_check(self.PAYMENT_SUMMARY)['data']['schoolQuery']['paymentSummary']
        self.assertEqual(
            content['outstandingBalance'],
            20000 - (100 * 10 + 200 * 20 + 300 * 30)
        )
        self.assertEqual(content['paymentCreditSum'], 40000)
        self.assertEqual(content['paymentDebitSum'], 20000)

        self.assertEqual(content['totalUnverifiedPayment'], 120000)
        self.assertEqual(content['totalUnverifiedPaymentCount'], 4)
        self.assertEqual(content['totalVerifiedPayment'], 40000)
        self.assertEqual(content['totalVerifiedPaymentCount'], 2)
