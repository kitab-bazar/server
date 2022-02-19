from utils.graphene.tests import GraphQLTestCase
from apps.user.factories import UserFactory
from apps.order.factories import CartItemFactory
from apps.book.factories import BookFactory, WishListFactory
from apps.publisher.factories import PublisherFactory


class TestOrder(GraphQLTestCase):
    def setUp(self):
        self.place_order_from_cart = '''
            mutation Mutation {
                placeOrderFromCart {
                    ok
                    errors
                }
            }
        '''

        self.cart = '''
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

        self.orders = '''
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

        self.retrieve_wish_list = '''
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
        content = self.query_check(self.cart)
        result = content['data']['cartItems']['results']
        self.assertEqual(len(result), 2)

        # Make sure wish list items exists
        content = self.query_check(self.retrieve_wish_list)
        result = content['data']['wishList']['results']
        self.assertEqual(len(result), 2)

        # Place order
        self.query_check(self.place_order_from_cart, okay=True)

        # Test should clear cart after order placed
        content = self.query_check(self.cart)
        result = content['data']['cartItems']['results']
        self.assertEqual(len(result), 0)

        # Test should clear wish list after order placed
        content = self.query_check(self.retrieve_wish_list)
        result = content['data']['wishList']['results']
        self.assertEqual(len(result), 0)

        # Test can retrieve orders
        content = self.query_check(self.orders)
        result = content['data']['orders']['results']
        total_price = 0
        for order in result:
            for book in order['bookOrders']['results']:
                total_price += book['quantity'] * book['price']

        self.assertEqual(
            total_price,
            self.book1.price * self.cart_item_1.quantity + self.book2.price * self.cart_item_2.quantity
        )
