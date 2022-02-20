from utils.graphene.tests import GraphQLTestCase

from apps.order.models import CartItem

from apps.order.serializers import CartItemSerializer
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
        user = UserFactory.create()
        book1 = BookFactory.create(publisher=self.publisher, price=10)
        book2 = BookFactory.create(publisher=self.publisher, price=20)

        self.force_login(user)
        # Test can create cart
        minput = {'book': book1.id, 'quantity': CartItemSerializer.MAX_ITEMS_ALLOWED + 1}
        # - Don't allow new item with > MAX_ITEMS_ALLOWED
        self.query_check(self.create_cart_item, minput=minput, okay=False)

        minput = {'book': book1.id, 'quantity': CartItemSerializer.MAX_ITEMS_ALLOWED}
        content = self.query_check(self.create_cart_item, minput=minput, okay=True)
        result = content['data']['createCartItem']['result']
        cart_item_1 = CartItem.objects.get(pk=result['id'])
        self.assertEqual(result['book']['id'], str(book1.id))
        self.assertEqual(result['quantity'], minput['quantity'])
        self.assertEqual(result['totalPrice'], minput['quantity'] * book1.price)

        # - Don't allow new item > MAX_ITEMS_ALLOWED
        minput = {'book': book2.id, 'quantity': 20}
        content = self.query_check(self.create_cart_item, minput=minput, okay=False)

        # Success if we change previous old cart item quantity
        cart_item_1.quantity = 1
        cart_item_1.save(update_fields=('quantity',))
        content = self.query_check(self.create_cart_item, minput=minput, okay=True)

        # Test can update cart item (Success)
        content = self.query_check(self.update_cart_item, minput=minput, variables={'id': cart_item_1.pk}, okay=True)
        result = content['data']['updateCartItem']['result']
        self.assertEqual(result['quantity'], minput['quantity'])
        self.assertEqual(result['totalPrice'], minput['quantity'] * book2.price)

        # Failure again for > MAX_ITEMS_ALLOWED
        minput = {'book': book2.id, 'quantity': CartItemSerializer.MAX_ITEMS_ALLOWED}
        self.query_check(self.update_cart_item, minput=minput, variables={'id': cart_item_1.pk}, okay=False)

        # Test can delete cart item
        # self.query_check(self.delete_cart_item, variables={'id': cart_id}, okay=True)

    def test_should_allow_to_add_same_book_mutiple_times_in_cart(self):
        self.force_login(self.user)

        # Add same book to cart 3 items
        self.query_check(
            self.create_cart_item,
            minput={'book': self.book.id, 'quantity': 2},
            okay=True
        )
        self.query_check(
            self.create_cart_item,
            minput={'book': self.book.id, 'quantity': 2},
            okay=False
        )
