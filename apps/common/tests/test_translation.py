from utils.graphene.tests import GraphQLTestCase
from apps.common.factories import DistrictFactory


class TestDistrict(GraphQLTestCase):
    def setUp(self):
        self.district_query = '''
            query MyQuery ($id: ID!) {
              district(id: $id) {
                id
                name
              }
            }
        '''
        super().setUp()

    def test_can_retrive_districts_without_authentication(self):
        district = DistrictFactory.create(name_en='english', name_ne='nepali')

        # test with header provided
        response = self.query_check(
            self.district_query,
            variables={'id': district.id},
            headers={'HTTP_ACCEPT_LANGUAGE': 'ne'}
        )
        self.assertEqual(response['data']['district']['name'], 'nepali')

        # test without header provided
        # should give the default name_en
        response = self.query_check(
            self.district_query,
            variables={'id': district.id},
        )
        self.assertEqual(response['data']['district']['name'], 'english')
