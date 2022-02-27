from apps.common.tests.test_permissions import TestPermissions

from apps.user.factories import UserFactory
from apps.book.factories import (
    AuthorFactory,
    CategoryFactory,
    TagFactory,
)


class TestBookCategoryPermissions(TestPermissions):
    TAGS_QUERY = '''
        query MyQuery($search: String) {
          tags(search: $search) {
            totalCount
            results {
              id
              name
            }
          }
        }
    '''

    AUTHOR_QUERY = '''
        query MyQuery($search: String) {
          authors(search: $search) {
            totalCount
            results {
              aboutAuthor
              id
              name
            }
          }
        }
    '''

    CATEGORY_QUERY = '''
        query MyQuery($search: String) {
          categories(search: $search) {
            totalCount
            results {
              id
              name
            }
          }
        }
    '''

    def setUp(self):
        super().setUp()
        self.user = UserFactory.create()

    def test_tags_query(self):
        tag1 = TagFactory.create(name_en='Animal', name_ne='Janawor')
        tag2 = TagFactory.create(name_en='Human hmm', name_ne='Manche')
        tag3 = TagFactory.create(name_en='Food hmm', name_ne='Khana')
        self.force_login(self.user)
        for search, expected_tags in [
            ('Animal', (tag1,)),
            ('janawor', (tag1,)),
            ('Khana', (tag3,)),
            ('hmm', (tag2, tag3)),
        ]:
            content = self.query_check(self.TAGS_QUERY, variables={'search': search})['data']['tags']
            self.assertEqual(content['totalCount'], len(expected_tags), (content, expected_tags))
            self.assertListIds(content['results'], expected_tags, (content, expected_tags))

    def test_authors_query(self):
        author1 = AuthorFactory.create(name_en='Animal', name_ne='Janawor')
        author2 = AuthorFactory.create(name_en='Human hmm', name_ne='Manche')
        author3 = AuthorFactory.create(name_en='Food hmm', name_ne='Khana')
        self.force_login(self.user)
        for search, expected_authors in [
            ('Animal', (author1,)),
            ('janawor', (author1,)),
            ('Khana', (author3,)),
            ('hmm', (author2, author3)),
        ]:
            content = self.query_check(self.AUTHOR_QUERY, variables={'search': search})['data']['authors']
            self.assertEqual(content['totalCount'], len(expected_authors), (content, expected_authors))
            self.assertListIds(content['results'], expected_authors, (content, expected_authors))

    def test_categories_query(self):
        category1 = CategoryFactory.create(name_en='Animal', name_ne='Janawor')
        category2 = CategoryFactory.create(name_en='Human hmm', name_ne='Manche')
        category3 = CategoryFactory.create(name_en='Food hmm', name_ne='Khana')
        self.force_login(self.user)
        for search, expected_categories in [
            ('Animal', (category1,)),
            ('janawor', (category1,)),
            ('Khana', (category3,)),
            ('hmm', (category2, category3)),
        ]:
            content = self.query_check(self.CATEGORY_QUERY, variables={'search': search})['data']['categories']
            self.assertEqual(content['totalCount'], len(expected_categories), (content, expected_categories))
            self.assertListIds(content['results'], expected_categories, (content, expected_categories))
