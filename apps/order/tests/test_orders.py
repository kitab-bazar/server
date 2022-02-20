from django.utils import timezone
from django.core.exceptions import ValidationError

from utils.graphene.tests import GraphQLTestCase

from apps.user.models import User
from apps.order.models import Order

from apps.user.factories import UserFactory
from apps.book.factories import BookFactory, WishListFactory
from apps.publisher.factories import PublisherFactory
from apps.order.factories import CartItemFactory, OrderWindowFactory, OrderFactory


class TestOrder(GraphQLTestCase):
    ENABLE_NOW_PATCHER = True

    CREATE_ORDER_FROM_CART_MUTATION = '''
        mutation Mutation {
            createOrderFromCart {
                ok
                errors
            }
        }
    '''

    UPDATE_ORDER_MUTATION = '''
        mutation Mutation($id: ID!, $input: OrderUpdateInputType!) {
          updateOrder(id: $id, data: $input) {
            ok
            result {
              id
              status
              activityLog {
                id
                comment
                createdAt
                createdBy {
                  id
                  fullName
                }
                systemGeneratedComment
              }
            }
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

    def test_can_create_order_form_cart(self):
        self.force_login(self.user)

        # Make sure cart items exists
        content = self.query_check(self.CART_QUERY)
        result = content['data']['cartItems']['results']
        self.assertEqual(len(result), 2)

        # Make sure wish list items exists
        content = self.query_check(self.WISH_LIST_QUERY)
        result = content['data']['wishList']['results']
        self.assertEqual(len(result), 2)

        # Create order (Without any order order window)
        self.query_check(self.CREATE_ORDER_FROM_CART_MUTATION, okay=False)

        # Create order (Without any active order window)
        OrderWindowFactory.create(
            start_date=self.now_datetime.date() - timezone.timedelta(20),
            end_date=self.now_datetime.date() - timezone.timedelta(10),
        )
        self.query_check(self.CREATE_ORDER_FROM_CART_MUTATION, okay=False)

        # Create order (With active order window)
        active_order_window = OrderWindowFactory.create(
            start_date=self.now_datetime.date() - timezone.timedelta(9),
            end_date=self.now_datetime.date() + timezone.timedelta(10),
        )
        self.query_check(self.CREATE_ORDER_FROM_CART_MUTATION, okay=True)

        # Test should clear cart after order created
        content = self.query_check(self.CART_QUERY)
        result = content['data']['cartItems']['results']
        self.assertEqual(len(result), 0)

        # Test should clear wish list after order created
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

    def test_order_update(self):
        school_user1 = UserFactory.create(user_type=User.UserType.SCHOOL_ADMIN)
        school_user2 = UserFactory.create(user_type=User.UserType.SCHOOL_ADMIN)
        moderator_user = UserFactory.create(user_type=User.UserType.MODERATOR)

        order1 = OrderFactory.create(created_by=school_user1)
        order2 = OrderFactory.create(created_by=school_user1, status=Order.Status.IN_TRANSIT)
        order3 = OrderFactory.create(created_by=school_user1, status=Order.Status.CANCELLED)
        order4 = OrderFactory.create(created_by=school_user1, status=Order.Status.COMPLETED)

        def _query_check(order, minput, **kwargs):
            return self.query_check(
                self.UPDATE_ORDER_MUTATION,
                minput=minput,
                variables={
                    'id': str(order.pk),
                },
                **kwargs,
            )

        # School2 all error
        self.force_login(school_user2)
        for order, status in [
            # ORDER 1 PENDING
            *(
                (order, status)
                for status in [Order.Status.IN_TRANSIT, Order.Status.COMPLETED, Order.Status.CANCELLED]
                for order in [order1, order2, order3, order4]
            ),
        ]:
            minput = {
                'status': status.name,
                'comment': f'Trying to change the status from {order.status} to {status}',
            }
            _query_check(order, minput, assert_for_error=True)

        # PENDING -> IN_TRANSIT is not allowed
        for order, status, user, okay in [
            # ORDER 1 PENDING
            (order1, Order.Status.CANCELLED, moderator_user, True),
            (order1, Order.Status.CANCELLED, school_user1, True),
            *(
                (order1, status, user, False)
                for status in [Order.Status.IN_TRANSIT, Order.Status.COMPLETED]
                for user in [school_user1, moderator_user]
            ),
            # ORDER 2 IN-TRANSIT
            *(
                (order2, status, school_user1, False)
                for status in [Order.Status.PENDING, Order.Status.COMPLETED, Order.Status.CANCELLED]
            ),
            # ORDER 3/4 CANCELLED/COMPLETED
            *(
                (order, status, user, False)
                for status in [Order.Status.PENDING, Order.Status.IN_TRANSIT, Order.Status.CANCELLED]
                for user in [school_user1, moderator_user]
                for order in [order3, order4]
            ),
        ]:
            self.force_login(user)
            minput = {
                'status': status.name,
                'comment': f'Trying to change the status from {order.status} to {status}',
            }
            response = _query_check(order, minput, okay=okay)
            if okay:
                assert len(response['data']['updateOrder']['result']['activityLog']) > 0
            order.save(update_fields=('status',))  # Revert back status for next user


class OrderWindowTest(GraphQLTestCase):
    ENABLE_NOW_PATCHER = True

    ORDER_WINDOW_QUERY = '''
        query OrderWindow {
          orderWindowActive {
            id
            startDate
            title
            endDate
            description
          }
        }
    '''

    def test_query(self):
        user = UserFactory.create()
        self.force_login(user)
        content = self.query_check(self.ORDER_WINDOW_QUERY)
        self.assertEqual(content['data']['orderWindowActive'], None)

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
            resp['data']['orderWindowActive'], dict(
                id=str(order_window.pk),
                title=order_window.title,
                description=order_window.description,
                startDate=order_window.start_date.isoformat(),
                endDate=order_window.end_date.isoformat(),
            )
        )
