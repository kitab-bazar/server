from utils.graphene.tests import GraphQLTestCase
from apps.book.factories import BookFactory
from apps.user.factories import UserFactory
from apps.publisher.factories import PublisherFactory


class TestCart(GraphQLTestCase):
    def setUp(self):
        self.create_cart_item = '''
            mutation Mutation($input: CartItemInputType!) {
                createCartItem(data: $input) {
                    ok
                    errors
                    result {
                      id
                      quantity
                      totalPrice
                      book {
                        id
                        title
                      }
                    }
                }
            }
        '''
        self.update_cart_item = '''
            mutation Mutation($id: ID!, $input: CartItemInputType!) {
                updateCartItem(id: $id data: $input) {
                    ok
                    errors
                    result {
                      id
                      quantity
                      totalPrice
                    }
                }
            }
        '''
        self.delete_cart_item = '''
            mutation Mutation($id: ID!) {
                deleteCartItem(id: $id) {
                    ok
                    errors
                }
            }
        '''
        self.retrieve_cart_items = '''
            query MyQuery {
              cartItems {
                results {
                  id
                  quantity
                  totalPrice
                  book {
                    id
                    price
                  }
                }
                grandTotalPrice
              }
            }
        '''
        self.user = UserFactory.create()
        self.publisher = PublisherFactory.create()
        self.book = BookFactory.create(publisher=self.publisher)
        super().setUp()

    def test_can_add_update_delete_cart_items(self):
        self.force_login(self.user)

        # Test can create cart
        minput = {'book': self.book.id, 'quantity': 2}
        content = self.query_check(self.create_cart_item, minput=minput, okay=True)
        result = content['data']['createCartItem']['result']
        self.assertEqual(result['book']['id'], str(self.book.id))
        self.assertEqual(result['quantity'], minput['quantity'])
        self.assertEqual(result['totalPrice'], minput['quantity'] * self.book.price)

        # Test can update cart item
        cart_id = result['id']
        minput = {'book': self.book.id, 'quantity': 20}
        content = self.query_check(
            self.update_cart_item, minput=minput, variables={'id': cart_id}, okay=True
        )
        result = content['data']['updateCartItem']['result']
        self.assertEqual(result['quantity'], minput['quantity'])
        self.assertEqual(result['totalPrice'], minput['quantity'] * self.book.price)

        # Test can delete cart item
        self.query_check(self.delete_cart_item, variables={'id': cart_id}, okay=True)

    def test_should_increase_quantity_if_same_book_is_added(self):
        self.force_login(self.user)

        # Add same book to cart 3 items
        for i in range(3):
            self.query_check(
                self.create_cart_item,
                minput={'book': self.book.id, 'quantity': 2},
                okay=True
            )

        # Retrieve cart
        content = self.query_check(self.retrieve_cart_items)
        result = content['data']['cartItems']['results']
        grand_total = content['data']['cartItems']['grandTotalPrice']
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['quantity'], 6)
        self.assertEqual(result[0]['totalPrice'], self.book.price * 6)
        self.assertEqual(grand_total, self.book.price * 6)
