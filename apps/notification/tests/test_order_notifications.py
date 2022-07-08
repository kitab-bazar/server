from utils.graphene.tests import GraphQLTestCase

from apps.user.models import User
from apps.order.models import Order
from apps.notification.models import Notification

from apps.user.factories import UserFactory
from apps.publisher.factories import PublisherFactory
from apps.book.factories import BookFactory
from apps.order.factories import BookOrderFactory, OrderFactory
from apps.book.models import Book


class TestNotificationForOrder(GraphQLTestCase):
    NOTIFICATIONS_QUERY = '''
        query Query {
          notifications {
            results {
              createdAt
              id
              notificationType
              read
              title
              order {
                status
              }
            }
            unreadCount
            readCount
            totalCount
          }
        }
    '''

    UPDATE_ORDER_QUERY = '''
    mutation Mutation($id: ID!, $input: OrderUpdateInputType!) {
        updateOrder(id: $id data: $input) {
            ok
            result {
                id
                status
            }
        }
    }
    '''

    def setUp(self):
        publisher = PublisherFactory.create()
        self.book = BookFactory.create(publisher=publisher)

        self.individual_user = UserFactory.create(user_type=User.UserType.INDIVIDUAL_USER)
        self.publisher_user = UserFactory.create(user_type=User.UserType.PUBLISHER)
        self.moderator_user = UserFactory.create(user_type=User.UserType.MODERATOR)

        # Attach publisher profile to publisher user
        self.publisher_user.publisher = publisher
        self.publisher_user.save()

        self.order = OrderFactory(created_by=self.individual_user)
        BookOrderFactory.create(
            book=self.book, order=self.order, quantity=1,
            grade=Book.Grade.GRADE_1.value, language=Book.LanguageType.ENGLISH.value
        )

        super().setUp()

    def test_customer_shoud_get_notification_if_order_cancelled(self):
        # Publisher updates order status
        self.force_login(self.moderator_user)
        minput = {'status': Order.Status.CANCELLED.name}
        with self.captureOnCommitCallbacks(execute=True):
            content = self.query_check(
                self.UPDATE_ORDER_QUERY, variables={'id': self.order.id}, minput=minput, okay=True
            )
        self.assertEqual(content['data']['updateOrder']['result']['status'], Order.Status.CANCELLED.name)

        # Test publisher should not get notification
        content = self.query_check(self.NOTIFICATIONS_QUERY)
        self.assertEqual(content['data']['notifications']['unreadCount'], 0)
        self.assertEqual(content['data']['notifications']['readCount'], 0)
        self.assertEqual(content['data']['notifications']['totalCount'], 0)
        self.assertEqual(len(content['data']['notifications']['results']), 0)

        # Test customer should get notification
        self.force_login(self.individual_user)
        content = self.query_check(self.NOTIFICATIONS_QUERY)
        notification_data = content['data']['notifications']['results'][0]
        self.assertEqual(notification_data['notificationType'], Notification.NotificationType.ORDER_CANCELLED.name)
        self.assertEqual(notification_data['read'], False)
        self.assertEqual(content['data']['notifications']['unreadCount'], 1)
        self.assertEqual(content['data']['notifications']['readCount'], 0)
        self.assertEqual(content['data']['notifications']['totalCount'], 1)

    def test_customer_shoud_get_notification_if_order_completed(self):
        order = OrderFactory(created_by=self.individual_user, status=Order.Status.IN_TRANSIT)
        # Publisher updates order status
        self.force_login(self.moderator_user)
        minput = {'status': Order.Status.COMPLETED.name}
        with self.captureOnCommitCallbacks(execute=True):
            content = self.query_check(self.UPDATE_ORDER_QUERY, variables={'id': order.id}, minput=minput, okay=True)
        self.assertEqual(content['data']['updateOrder']['result']['status'], Order.Status.COMPLETED.name)

        # Test publisher should not get notification
        content = self.query_check(self.NOTIFICATIONS_QUERY)
        self.assertEqual(content['data']['notifications']['unreadCount'], 0)
        self.assertEqual(content['data']['notifications']['readCount'], 0)
        self.assertEqual(content['data']['notifications']['totalCount'], 0)
        self.assertEqual(len(content['data']['notifications']['results']), 0)

        # Test customer should get notification
        self.force_login(self.individual_user)
        content = self.query_check(self.NOTIFICATIONS_QUERY)
        notificaiton_data = content['data']['notifications']['results'][0]
        self.assertEqual(notificaiton_data['notificationType'], Notification.NotificationType.ORDER_COMPLETED.name)
        self.assertEqual(notificaiton_data['read'], False)
        self.assertEqual(content['data']['notifications']['unreadCount'], 1)
        self.assertEqual(content['data']['notifications']['readCount'], 0)
        self.assertEqual(content['data']['notifications']['totalCount'], 1)
