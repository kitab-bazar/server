from utils.graphene.tests import GraphQLTestCase
from apps.user.factories import UserFactory
from django.contrib.auth.hashers import check_password
from apps.user.models import User


class TestUser(GraphQLTestCase):
    def setUp(self):
        self.register_mutation = '''
            mutation Mutation($input: RegisterInputType!) {
                register(data: $input) {
                    ok
                    result {
                        email
                        id
                        firstName
                        lastName
                        fullName
                    }
                }
            }
        '''
        self.login_mutation = '''
        mutation Mutation($input: LoginInputType!) {
            login(data: $input) {
                ok
                result {
                    email
                    id
                }
            }
        }
        '''
        self.change_password_mutation = '''
            mutation Mutation($input: ChangePasswordInputType!) {
                changePassword(data: $input) {
                    ok
                    result {
                        email
                    }
                }
            }
        '''
        self.logout_mutation = '''
            mutation Mutation {
              logout {
                ok
              }
            }
        '''
        super().setUp()

    def test_register_individual_user(self):
        minput = {
            "firstName": "Rosy", "lastName": "Rosy", "email": "rosy@gmail.com",
            "password": "nsPzXEVKGCIriVu", "userType": User.UserType.INDIVIDUAL_USER.name, "profile": {}
        }
        content = self.query_check(self.register_mutation, minput=minput, okay=True)
        first_name = content['data']['register']['result']['firstName']
        last_name = content['data']['register']['result']['lastName']
        self.assertEqual(first_name, minput['firstName'], content)
        self.assertEqual(last_name, minput['lastName'], content)
        self.assertEqual(content['data']['register']['result']['fullName'], f'{first_name} {last_name}', content)
        self.assertEqual(content['data']['register']['result']['email'], minput['email'], content)

    def test_login(self):
        # Test invaid user should not login
        minput = {"email": "alex@gmail.com", "password": "rupoFpCyZVaNMjY"}
        self.query_check(self.login_mutation, minput=minput, okay=False)

        # Test valid user should login
        user = UserFactory.create(email=minput['email'])
        minput = {"email": user.email, "password": user.password_text}
        content = self.query_check(self.login_mutation, minput=minput, okay=True)
        self.assertEqual(content['data']['login']['result']['id'], str(user.id), content)
        self.assertEqual(content['data']['login']['result']['email'], user.email, content)

    def test_change_password(self):
        user = UserFactory.create()
        self.force_login(user)
        new_password = "INZbHBhOyCqurWt"

        # Test should not change password if old password not matched
        minput = {"oldPassword": 'random-passsword', "newPassword": new_password}
        self.query_check(self.change_password_mutation, minput=minput, okay=False)
        user.refresh_from_db()
        self.assertFalse(check_password(new_password, user.password))

        # Test should change password
        minput = {"oldPassword": user.password_text, "newPassword": new_password}
        self.query_check(self.change_password_mutation, minput=minput, okay=True)
        user.refresh_from_db()
        self.assertTrue(check_password(new_password, user.password))

    def test_logout(self):
        self.query_check(self.logout_mutation, okay=True)
