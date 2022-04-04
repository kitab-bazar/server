from utils.graphene.tests import GraphQLTestCase
from apps.publisher.factories import PublisherFactory
from apps.book.factories import BookFactory


class TestBookEnumTranslation(GraphQLTestCase):
    def setUp(self):
        self.book_query = '''
            query GradeOptions {
              gradeList: __type(name: "BookGradeEnum") {
                enumValues {
                  name
                  description
                }
              }
            }
        '''
        super().setUp()

    def test_should_translate_book_enums(self):
        publisher = PublisherFactory.create()
        district = BookFactory.create(publisher=publisher)

        response = self.query_check(
            self.book_query,
            variables={'id': district.id},
            headers={'HTTP_ACCEPT_LANGUAGE': 'ne'}
        )
        self.assertEqual(response['data']['gradeList']['enumValues'][0]['description'], 'कक्षा १')

        response = self.query_check(
            self.book_query,
            variables={'id': district.id},
            headers={'HTTP_ACCEPT_LANGUAGE': 'en'}
        )
        self.assertEqual(response['data']['gradeList']['enumValues'][0]['description'], 'Grade 1')
