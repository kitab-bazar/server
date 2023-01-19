from utils.graphene.tests import GraphQLTestCase
from apps.book.models import Book

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
        grade_1_translated_text = None
        for enum in response['data']['gradeList']['enumValues']:
            if enum['name'] == Book.Grade.GRADE_1.name:
                grade_1_translated_text = enum['description']

        self.assertEqual(grade_1_translated_text, 'कक्षा १')

        response = self.query_check(
            self.book_query,
            variables={'id': district.id},
            headers={'HTTP_ACCEPT_LANGUAGE': 'en'}
        )
        for enum in response['data']['gradeList']['enumValues']:
            if enum['name'] == Book.Grade.GRADE_1.name:
                grade_1_translated_text = enum['description']
        self.assertEqual(grade_1_translated_text, 'Grade 1')
