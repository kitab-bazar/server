from utils.graphene.tests import GraphQLTestCase

from apps.user.models import User
from apps.order.models import Order
from apps.notification.models import Notification

from apps.user.factories import UserFactory
from apps.publisher.factories import PublisherFactory
from apps.book.factories import BookFactory
from apps.order.factories import BookOrderFactory, OrderFactory


class TestNotificationForOrder(GraphQLTestCase):
    def setUp(self):
        self.notifications = '''
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
        self.update_order = '''
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
        publisher = PublisherFactory.create()
        self.book = BookFactory.create(publisher=publisher)

        self.individual_user = UserFactory.create(user_type=User.UserType.INDIVIDUAL_USER)
        self.publisher_user = UserFactory.create(user_type=User.UserType.PUBLISHER)

        # Attach publisher profile to publisher user
        self.publisher_user.publisher = publisher
        self.publisher_user.save()

        self.order = OrderFactory(created_by=self.individual_user)
        BookOrderFactory.create(book=self.book, order=self.order, publisher=publisher)

        super().setUp()

    def test_pulisher_should_get_notification_if_order_placed(self):
        self.force_login(self.publisher_user)
        minput = {'status': Order.Status.RECEIVED.name}
        with self.captureOnCommitCallbacks(execute=True):
            content = self.query_check(self.update_order, variables={'id': self.order.id}, minput=minput, okay=True)
        self.assertEqual(content['data']['updateOrder']['result']['status'], Order.Status.RECEIVED.name)

        # Test customer (individual_user) should not get notification
        self.force_login(self.individual_user)
        content = self.query_check(self.notifications)
        self.assertEqual(content['data']['notifications']['unreadCount'], 0)
        self.assertEqual(content['data']['notifications']['readCount'], 0)
        self.assertEqual(content['data']['notifications']['totalCount'], 0)
        self.assertEqual(len(content['data']['notifications']['results']), 0)

        # Test publisher should get notification
        self.force_login(self.publisher_user)
        content = self.query_check(self.notifications)
        notificaiton_data = content['data']['notifications']['results'][0]
        self.assertEqual(notificaiton_data['notificationType'], Notification.NotificationType.ORDER_RECEIVED.name)
        self.assertEqual(notificaiton_data['read'], False)
        self.assertEqual(content['data']['notifications']['unreadCount'], 1)
        self.assertEqual(content['data']['notifications']['readCount'], 0)
        self.assertEqual(content['data']['notifications']['totalCount'], 1)

    def test_customer_shoud_get_notification_if_order_cancelled(self):
        # Publisher updates order status
        self.force_login(self.publisher_user)
        minput = {'status': Order.Status.CANCELLED.name}
        with self.captureOnCommitCallbacks(execute=True):
            content = self.query_check(self.update_order, variables={'id': self.order.id}, minput=minput, okay=True)
        self.assertEqual(content['data']['updateOrder']['result']['status'], Order.Status.CANCELLED.name)

        # Test publisher should not get notification
        content = self.query_check(self.notifications)
        self.assertEqual(content['data']['notifications']['unreadCount'], 0)
        self.assertEqual(content['data']['notifications']['readCount'], 0)
        self.assertEqual(content['data']['notifications']['totalCount'], 0)
        self.assertEqual(len(content['data']['notifications']['results']), 0)

        # Test customer should get notification
        self.force_login(self.individual_user)
        content = self.query_check(self.notifications)
        notificaiton_data = content['data']['notifications']['results'][0]
        self.assertEqual(notificaiton_data['notificationType'], Notification.NotificationType.ORDER_CANCELLED.name)
        self.assertEqual(notificaiton_data['read'], False)
        self.assertEqual(content['data']['notifications']['unreadCount'], 1)
        self.assertEqual(content['data']['notifications']['readCount'], 0)
        self.assertEqual(content['data']['notifications']['totalCount'], 1)

    def test_customer_shoud_get_notification_if_order_packed(self):
        # Publisher updates order status
        self.force_login(self.publisher_user)
        minput = {'status': Order.Status.PACKED.name}
        with self.captureOnCommitCallbacks(execute=True):
            content = self.query_check(self.update_order, variables={'id': self.order.id}, minput=minput, okay=True)
        self.assertEqual(content['data']['updateOrder']['result']['status'], Order.Status.PACKED.name)

        # Test publisher should not get notification
        content = self.query_check(self.notifications)
        self.assertEqual(content['data']['notifications']['unreadCount'], 0)
        self.assertEqual(content['data']['notifications']['readCount'], 0)
        self.assertEqual(content['data']['notifications']['totalCount'], 0)
        self.assertEqual(len(content['data']['notifications']['results']), 0)

        # Test customer should get notification
        self.force_login(self.individual_user)
        content = self.query_check(self.notifications)
        notificaiton_data = content['data']['notifications']['results'][0]
        self.assertEqual(notificaiton_data['notificationType'], Notification.NotificationType.ORDER_PACKED.name)
        self.assertEqual(notificaiton_data['read'], False)
        self.assertEqual(content['data']['notifications']['unreadCount'], 1)
        self.assertEqual(content['data']['notifications']['readCount'], 0)
        self.assertEqual(content['data']['notifications']['totalCount'], 1)

    def test_customer_shoud_get_notification_if_order_completed(self):
        # Publisher updates order status
        self.force_login(self.publisher_user)
        minput = {'status': Order.Status.COMPLETED.name}
        with self.captureOnCommitCallbacks(execute=True):
            content = self.query_check(self.update_order, variables={'id': self.order.id}, minput=minput, okay=True)
        self.assertEqual(content['data']['updateOrder']['result']['status'], Order.Status.COMPLETED.name)

        # Test publisher should not get notification
        content = self.query_check(self.notifications)
        self.assertEqual(content['data']['notifications']['unreadCount'], 0)
        self.assertEqual(content['data']['notifications']['readCount'], 0)
        self.assertEqual(content['data']['notifications']['totalCount'], 0)
        self.assertEqual(len(content['data']['notifications']['results']), 0)

        # Test customer should get notification
        self.force_login(self.individual_user)
        content = self.query_check(self.notifications)
        notificaiton_data = content['data']['notifications']['results'][0]
        self.assertEqual(notificaiton_data['notificationType'], Notification.NotificationType.ORDER_COMPLETED.name)
        self.assertEqual(notificaiton_data['read'], False)
        self.assertEqual(content['data']['notifications']['unreadCount'], 1)
        self.assertEqual(content['data']['notifications']['readCount'], 0)
        self.assertEqual(content['data']['notifications']['totalCount'], 1)
