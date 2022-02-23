from utils.graphene.tests import GraphQLTestCase

from apps.user.models import User

from apps.user.factories import UserFactory
from apps.publisher.factories import PublisherFactory
from apps.school.factories import SchoolFactory
from apps.institution.factories import InstitutionFactory


class UserQueryTest(GraphQLTestCase):
    USER_QUERY = '''
        query MyQuery {
          users(ordering: "id") {
            results {
              id
              fullName
              canonicalName
            }
            totalCount
          }
        }
    '''

    def test_user_canonical_name(self):
        user = UserFactory.create(first_name='', last_name='')
        publisher_user = UserFactory.create(
            user_type=User.UserType.PUBLISHER,
            publisher=PublisherFactory.create(),
        )
        school_user = UserFactory.create(
            user_type=User.UserType.SCHOOL_ADMIN,
            school=SchoolFactory.create(),
        )
        school_user_without_school = UserFactory.create(user_type=User.UserType.SCHOOL_ADMIN)
        institution_user = UserFactory.create(
            user_type=User.UserType.INSTITUTIONAL_USER,
            institution=InstitutionFactory.create(),
        )
        institution_user_without_institution = UserFactory.create(user_type=User.UserType.INSTITUTIONAL_USER)
        moderator_user = UserFactory.create()
        individual_user = UserFactory.create()
        self.force_login(user)

        # Make sure cart items exists
        content = self.query_check(self.USER_QUERY)['data']['users']['results']
        self.assertEqual(content, [
            dict(
                id=str(user.id),
                fullName=str(user.full_name),
                canonicalName=expected_name,
            ) for user, expected_name in [
                (user, user.full_name),
                (publisher_user, publisher_user.publisher.name),
                (school_user, school_user.school.name),
                (school_user_without_school, school_user_without_school.full_name),
                (institution_user, institution_user.institution.name),
                (institution_user_without_institution, institution_user_without_institution.full_name),
                (moderator_user, moderator_user.full_name),
                (individual_user, individual_user.full_name),
            ]
        ])
