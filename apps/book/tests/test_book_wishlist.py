from utils.graphene.tests import GraphQLTestCase
from apps.book.factories import BookFactory
from apps.user.factories import UserFactory
from apps.publisher.factories import PublisherFactory


class TestWishList(GraphQLTestCase):
    def setUp(self):
        self.wish_list_mutation = '''
            mutation Mutation($input: WishListInputType!) {
                createWishlist(data: $input) {
                    ok
                    errors
                    result {
                      id
                      book {
                        id
                      }
                    }
                }
            }
        '''
        self.wish_list_query = '''
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
        super().setUp()

    def test_wish_list(self):
        user = UserFactory.create()
        self.force_login(user)
        publisher = PublisherFactory.create()
        book = BookFactory.create(publisher=publisher)
        minput = {'book': book.id}
        content = self.query_check(self.wish_list_mutation, minput=minput, okay=True)
        book_id = content['data']['createWishlist']['result']['book']['id']
        self.assertEqual(str(book.id), book_id)

        # Should not add same books multiple times in wish list
        self.query_check(self.wish_list_mutation, minput=minput, okay=False)

        # Test should retrieve wishlist
        content = self.query_check(self.wish_list_query)
        self.assertEqual(content['data']['wishList']['results'][0]['book']['id'], str(book.id))

        # Test should not retrieve wishlist of another user
        user_2 = UserFactory.create()
        self.force_login(user_2)
        content = self.query_check(self.wish_list_query)
        self.assertFalse(content['data']['wishList']['results'], [])
