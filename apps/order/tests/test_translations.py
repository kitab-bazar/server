from utils.graphene.tests import GraphQLTestCase

from apps.user.models import User
from apps.order.models import Order

from apps.user.factories import UserFactory
from apps.book.factories import BookFactory
from apps.order.factories import OrderFactory, BookOrderFactory
from apps.publisher.factories import PublisherFactory


class TestOrderTranslation(GraphQLTestCase):
    def setUp(self):
        self.orders_query = '''
            query MyQuery {
              orders {
                results {
                  bookOrders {
                    results {
                      price
                      quantity
                      title
                    }
                  }
                  totalPrice
                  totalQuantity
                }
              }
            }
        '''
        self.admin_user = UserFactory.create(user_type=User.UserType.MODERATOR.value)
        self.individual_user = UserFactory.create(user_type=User.UserType.INDIVIDUAL_USER.value)
        publisher = PublisherFactory.create()
        self.book = BookFactory.create(publisher=publisher)
        order = OrderFactory.create(created_by=self.individual_user, status=Order.Status.COMPLETED)
        BookOrderFactory.create(
            order=order, publisher=publisher, book=self.book,
            title_en='book title in english',
            title_ne='book title in nepali',
        )
        super().setUp()

    def test_can_retrive_districts_without_authentication(self):
        # test with header provided
        self.force_login(self.admin_user)
        content = self.query_check(
            self.orders_query,
            headers={'HTTP_ACCEPT_LANGUAGE': 'ne'}
        )
        title = content['data']['orders']['results'][0]['bookOrders']['results'][0]['title']
        self.assertEqual(title, 'book title in nepali')
        content = self.query_check(
            self.orders_query,
            headers={'HTTP_ACCEPT_LANGUAGE': 'en'}
        )
        title = content['data']['orders']['results'][0]['bookOrders']['results'][0]['title']
        self.assertEqual(title, 'book title in english')
