from utils.graphene.tests import GraphQLTestCase

from apps.user.models import User
from apps.order.models import Order

from apps.user.factories import UserFactory
from apps.book.factories import BookFactory
from apps.order.factories import OrderFactory, BookOrderFactory
from apps.publisher.factories import PublisherFactory


class TestOrderTranslation(GraphQLTestCase):
    ORDERS_QUERY = '''
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

    def test_can_retrive_book_detail_from_order_after_change(self):
        moderator_user = UserFactory.create(user_type=User.UserType.MODERATOR.value)
        user = UserFactory.create(user_type=User.UserType.SCHOOL_ADMIN.value)
        publisher = PublisherFactory.create()
        self.book = BookFactory.create(
            publisher=publisher,
            title_en='book title in english',
            title_ne='book title in nepali',
        )
        order = OrderFactory.create(created_by=user, status=Order.Status.COMPLETED)
        # Creatign a order here
        BookOrderFactory.create(order=order, book=self.book, quantity=1)
        # Changing the title here
        self.book.title_en = 'new book title in english'
        self.book.title_ne = 'new book title in nepali'
        self.book.save(update_fields=('title_en', 'title_ne'))
        # test with header provided
        self.force_login(moderator_user)
        content = self.query_check(
            self.ORDERS_QUERY,
            headers={'HTTP_ACCEPT_LANGUAGE': 'ne'}
        )
        title = content['data']['orders']['results'][0]['bookOrders']['results'][0]['title']
        self.assertEqual(title, 'book title in nepali')
        content = self.query_check(
            self.ORDERS_QUERY,
            headers={'HTTP_ACCEPT_LANGUAGE': 'en'}
        )
        title = content['data']['orders']['results'][0]['bookOrders']['results'][0]['title']
        self.assertEqual(title, 'book title in english')
