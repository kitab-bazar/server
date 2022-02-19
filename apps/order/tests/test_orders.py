from django.utils import timezone
from django.core.exceptions import ValidationError

from utils.graphene.tests import GraphQLTestCase
from apps.user.factories import UserFactory
from apps.book.factories import BookFactory, WishListFactory
from apps.publisher.factories import PublisherFactory

from apps.order.factories import CartItemFactory, OrderWindowFactory, Order


class TestOrder(GraphQLTestCase):
    ENABLE_NOW_PATCHER = True

    PLACE_ORDER_FROM_CART_MUTATION = '''
        mutation Mutation {
            placeOrderFromCart {
                ok
                errors
            }
        }
    '''

    CART_QUERY = '''
        query MyQuery {
          cartItems {
            results {
              id
              totalPrice
            }
            grandTotalPrice
          }
        }
    '''

    ORDERS_QUERY = '''
        query MyQuery {
          orders {
            results {
              id
              totalPrice
              bookOrders {
                results {
                  id
                  quantity
                  price
                }
              }
            }
          }
        }
    '''

    WISH_LIST_QUERY = '''
        query MyQuery {
          wishList {
            results {
              id
              book {
                id
              }
            }
          }
        }
    '''

    def setUp(self):
        self.user = UserFactory.create()
        publisher = PublisherFactory.create()
        self.book1, self.book2 = BookFactory.create_batch(2, publisher=publisher)
        self.cart_item_1 = CartItemFactory.create(book=self.book1, created_by=self.user)
        self.cart_item_2 = CartItemFactory.create(book=self.book2, created_by=self.user)
        self.wish_list_1 = WishListFactory.create(book=self.book1, created_by=self.user)
        self.wish_list_2 = WishListFactory.create(book=self.book2, created_by=self.user)

        super().setUp()

    def test_can_place_order_form_cart(self):
        self.force_login(self.user)

        # Make sure cart items exists
        content = self.query_check(self.CART_QUERY)
        result = content['data']['cartItems']['results']
        self.assertEqual(len(result), 2)

        # Make sure wish list items exists
        content = self.query_check(self.WISH_LIST_QUERY)
        result = content['data']['wishList']['results']
        self.assertEqual(len(result), 2)

        # Place order (Without any order order window)
        self.query_check(self.PLACE_ORDER_FROM_CART_MUTATION, okay=False)

        # Place order (Without any active order window)
        OrderWindowFactory.create(
            start_date=self.now_datetime.date() - timezone.timedelta(20),
            end_date=self.now_datetime.date() - timezone.timedelta(10),
        )
        self.query_check(self.PLACE_ORDER_FROM_CART_MUTATION, okay=False)

        # Place order (With active order window)
        active_order_window = OrderWindowFactory.create(
            start_date=self.now_datetime.date() - timezone.timedelta(9),
            end_date=self.now_datetime.date() + timezone.timedelta(10),
        )
        self.query_check(self.PLACE_ORDER_FROM_CART_MUTATION, okay=True)

        # Test should clear cart after order placed
        content = self.query_check(self.CART_QUERY)
        result = content['data']['cartItems']['results']
        self.assertEqual(len(result), 0)

        # Test should clear wish list after order placed
        content = self.query_check(self.WISH_LIST_QUERY)
        result = content['data']['wishList']['results']
        self.assertEqual(len(result), 0)

        # Test can retrieve orders
        content = self.query_check(self.ORDERS_QUERY)
        resp_orders = content['data']['orders']['results']
        total_price = 0
        for order in resp_orders:
            self.assertEqual(Order.objects.get(pk=order['id']).assigned_order_window.pk, active_order_window.pk)
            for book in order['bookOrders']['results']:
                total_price += book['quantity'] * book['price']

        self.assertEqual(
            total_price,
            self.book1.price * self.cart_item_1.quantity + self.book2.price * self.cart_item_2.quantity
        )


class OrderWindowTest(GraphQLTestCase):
    ENABLE_NOW_PATCHER = True

    ORDER_WINDOW_QUERY = '''
        query OrderWindow {
          orderWindow {
            id
            startDate
            title
            endDate
            description
          }
        }
    '''

    def test_query(self):
        content = self.query_check(self.ORDER_WINDOW_QUERY)
        self.assertEqual(content['data']['orderWindow'], None)

        # This should throw error as end_date < start_date
        with self.assertRaises(ValidationError):
            OrderWindowFactory.create(
                start_date=self.now_datetime.date() + timezone.timedelta(10),
                end_date=self.now_datetime.date() - timezone.timedelta(10),
            )
        # In different window -20 -10
        OrderWindowFactory.create(
            start_date=self.now_datetime.date() - timezone.timedelta(20),
            end_date=self.now_datetime.date() - timezone.timedelta(10),
        )
        # Current -9 +10
        order_window = OrderWindowFactory.create(
            start_date=self.now_datetime.date() - timezone.timedelta(9),
            end_date=self.now_datetime.date() + timezone.timedelta(10),
        )
        # In different window +10 +30 (This should throw error)
        with self.assertRaises(ValidationError):
            OrderWindowFactory.create(
                start_date=self.now_datetime.date() + timezone.timedelta(10),
                end_date=self.now_datetime.date() + timezone.timedelta(30),
            )
        # In different window +11 +30 (this shouldn't throw any error)
        OrderWindowFactory.create(
            start_date=self.now_datetime.date() + timezone.timedelta(11),
            end_date=self.now_datetime.date() + timezone.timedelta(30),
        )
        # Updating this shouldn't throw any error. (Exclude itself while validating)
        order_window.save()

        resp = self.query_check(self.ORDER_WINDOW_QUERY)
        self.assertEqual(
            resp['data']['orderWindow'], dict(
                id=str(order_window.pk),
                title=order_window.title,
                description=order_window.description,
                startDate=order_window.start_date.isoformat(),
                endDate=order_window.end_date.isoformat(),
            )
        )
