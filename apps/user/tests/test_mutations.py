import mock
from django.contrib.auth.hashers import check_password
from django.test import override_settings

from utils.graphene.tests import GraphQLTestCase

from apps.user.models import User
from apps.user.factories import UserFactory
from apps.common.factories import MunicipalityFactory
from apps.school.factories import SchoolFactory
from apps.publisher.factories import PublisherFactory
from apps.institution.factories import InstitutionFactory


class TestUser(GraphQLTestCase):
    def setUp(self):
        self.register_mutation = '''
            mutation Mutation($input: RegisterInputType!) {
                register(data: $input) {
                    ok
                    result {
                        id
                        firstName
                        lastName
                        fullName
                        isActive
                    }
                    errors
                }
            }
        '''
        self.login_mutation = '''
        mutation Mutation($input: LoginInputType!) {
            login(data: $input) {
                ok
                result {
                    id
                }
                errors
                captchaRequired
            }
        }
        '''
        self.change_password_mutation = '''
            mutation Mutation($input: ChangePasswordInputType!) {
                changePassword(data: $input) {
                    ok
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
        self.update_profile = '''
            mutation Mutation($input: UpdateProfileType!) {
                updateProfile(data: $input) {
                    ok
                    errors
                    result {
                      firstName
                      fullName
                      lastName
                      userType
                      phoneNumber
                      school {
                        localAddress
                        name
                        wardNumber
                      }
                      institution {
                        localAddress
                        name
                        wardNumber
                      }
                      publisher {
                        localAddress
                        name
                        wardNumber
                      }
                    }
                }
            }
        '''
        self.verify_user = '''
            mutation MyMutation($id: ID!) {
                moderatorMutation {
                    userVerify(id: $id) {
                        errors
                        ok
                        result {
                            id
                            fullName
                            isActive
                            userType
                            isVerified
                        }
                    }
                }
            }
        '''

        self.municipality = MunicipalityFactory.create()
        self.user = UserFactory.create(user_type=User.UserType.INDIVIDUAL_USER)
        super().setUp()

    @mock.patch('apps.user.serializers.validate_hcaptcha')
    def test_register_individual_user(self, validate_captcha):
        validate_captcha.return_value = True
        minput = {
            "firstName": "Rosy", "lastName": "Rosy", "email": "rosy@gmail.com",
            "password": "nsPzXEVKGCIriVu", "userType": User.UserType.INDIVIDUAL_USER.name,
            'captcha': '11111111111', 'siteKey': '2222222222222',
        }
        content = self.query_check(self.register_mutation, minput=minput, okay=True)
        first_name = content['data']['register']['result']['firstName']
        last_name = content['data']['register']['result']['lastName']
        is_active = content['data']['register']['result']['isActive']
        self.assertEqual(first_name, minput['firstName'], content)
        self.assertEqual(last_name, minput['lastName'], content)
        self.assertTrue(is_active)
        self.assertEqual(content['data']['register']['result']['fullName'], f'{first_name} {last_name}', content)

    def test_login(self):
        # Test invaid user should not login
        minput = {"email": "alex@gmail.com", "password": "rupoFpCyZVaNMjY"}
        self.query_check(self.login_mutation, minput=minput, okay=False)

        # Test valid user should login
        user = UserFactory.create(email=minput['email'])
        minput = {"email": user.email, "password": user.password_text}
        content = self.query_check(self.login_mutation, minput=minput, okay=True)
        self.assertEqual(content['data']['login']['result']['id'], str(user.id), content)

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

    def test_individual_user_can_update_profile(self):
        user = UserFactory.create(user_type=User.UserType.INDIVIDUAL_USER.value)
        self.force_login(user)
        minput = {"firstName": 'Bimal', "lastName": 'Pandey', 'phoneNumber': '9848864675'}
        response = self.query_check(self.update_profile, minput=minput, okay=True)
        content = response['data']['updateProfile']['result']
        self.assertEqual(content['firstName'], minput['firstName'])
        self.assertEqual(content['lastName'], minput['lastName'])
        # NOTE: +977 prefix is added by phonenumberfield
        self.assertEqual(content['phoneNumber'], '+977' + minput['phoneNumber'])
        self.assertEqual(content['fullName'], minput['firstName'] + ' ' + minput['lastName'])
        self.assertEqual(content['userType'], User.UserType.INDIVIDUAL_USER.name)
        self.assertEqual(content['school'], None)
        self.assertEqual(content['publisher'], None)
        self.assertEqual(content['institution'], None)

    def test_school_admin_can_update_profile(self):
        school = SchoolFactory.create()
        user = UserFactory.create(user_type=User.UserType.SCHOOL_ADMIN.value, school=school)
        self.force_login(user)
        minput = {
            "firstName": 'Bimal', "lastName": 'Pandey', 'phoneNumber': '9848864611',
            'school': {
                'localAddress': 'Kanchanpur', 'name': 'XYZ', 'wardNumber': '8',
                'municipality': self.municipality.id
            }
        }
        response = self.query_check(self.update_profile, minput=minput, okay=True)
        content = response['data']['updateProfile']['result']
        self.assertEqual(content['firstName'], minput['firstName'])
        self.assertEqual(content['lastName'], minput['lastName'])
        # NOTE: +977 prefix is added by phonenumberfield
        self.assertEqual(content['phoneNumber'], '+977' + minput['phoneNumber'])
        self.assertEqual(content['fullName'], minput['firstName'] + ' ' + minput['lastName'])
        self.assertEqual(content['userType'], User.UserType.SCHOOL_ADMIN.name)
        self.assertEqual(content['school']['localAddress'], minput['school']['localAddress'])
        self.assertEqual(content['school']['name'], minput['school']['name'])
        self.assertEqual(str(content['school']['wardNumber']), minput['school']['wardNumber'])
        self.assertEqual(content['publisher'], None)
        self.assertEqual(content['institution'], None)
        # Test can update multiple times
        self.query_check(self.update_profile, minput=minput, okay=True)

    def test_institution_user_can_update_profile(self):
        institution = InstitutionFactory.create()
        user = UserFactory.create(user_type=User.UserType.INSTITUTIONAL_USER.value, institution=institution)
        self.force_login(user)
        minput = {
            "firstName": 'Bimal', "lastName": 'Pandey', 'phoneNumber': '9848864622',
            'institution': {
                'localAddress': 'Kanchanpur', 'name': 'XYZ', 'wardNumber': '8',
                'municipality': self.municipality.id
            }
        }
        response = self.query_check(self.update_profile, minput=minput, okay=True)
        content = response['data']['updateProfile']['result']
        self.assertEqual(content['firstName'], minput['firstName'])
        self.assertEqual(content['lastName'], minput['lastName'])
        # NOTE: +977 prefix is added by phonenumberfield
        self.assertEqual(content['phoneNumber'], '+977' + minput['phoneNumber'])
        self.assertEqual(content['fullName'], minput['firstName'] + ' ' + minput['lastName'])
        self.assertEqual(content['userType'], User.UserType.INSTITUTIONAL_USER.name)
        self.assertEqual(content['institution']['localAddress'], minput['institution']['localAddress'])
        self.assertEqual(content['institution']['name'], minput['institution']['name'])
        self.assertEqual(str(content['institution']['wardNumber']), minput['institution']['wardNumber'])
        self.assertEqual(content['publisher'], None)
        self.assertEqual(content['school'], None)
        # Test can update multiple times
        self.query_check(self.update_profile, minput=minput, okay=True)

    def test_publisher_user_can_update_profile(self):
        publisher = PublisherFactory.create()
        user = UserFactory.create(user_type=User.UserType.PUBLISHER.value, publisher=publisher)
        self.force_login(user)
        minput = {
            "firstName": 'Bimal', "lastName": 'Pandey', 'phoneNumber': '9848864633',
            'publisher': {
                'localAddress': 'Kanchanpur', 'name': 'XYZ', 'wardNumber': '8',
                'municipality': self.municipality.id
            }
        }
        response = self.query_check(self.update_profile, minput=minput, okay=True)
        content = response['data']['updateProfile']['result']
        self.assertEqual(content['firstName'], minput['firstName'])
        self.assertEqual(content['lastName'], minput['lastName'])
        # NOTE: +977 prefix is added by phonenumberfield
        self.assertEqual(content['phoneNumber'], '+977' + minput['phoneNumber'])
        self.assertEqual(content['fullName'], minput['firstName'] + ' ' + minput['lastName'])
        self.assertEqual(content['userType'], User.UserType.PUBLISHER.name)
        self.assertEqual(content['publisher']['localAddress'], minput['publisher']['localAddress'])
        self.assertEqual(content['publisher']['name'], minput['publisher']['name'])
        self.assertEqual(str(content['publisher']['wardNumber']), minput['publisher']['wardNumber'])
        self.assertEqual(content['institution'], None)
        self.assertEqual(content['school'], None)
        # Test can update multiple times
        self.query_check(self.update_profile, minput=minput, okay=True)

    def test_verify_user(self):
        user = UserFactory.create(user_type=User.UserType.INDIVIDUAL_USER.value, is_verified=False)
        school_user = UserFactory.create(user_type=User.UserType.SCHOOL_ADMIN.value)
        moderator = UserFactory.create(user_type=User.UserType.MODERATOR.value)

        # test : school admin cannot verify user
        self.force_login(school_user)

        def _query_check(**kwargs):
            return self.query_check(self.verify_user, variables={'id': str(user.id)}, **kwargs)

        self.assertEqual(user.is_verified, False)
        self.assertEqual(user.verified_by, None)
        _query_check(assert_for_error=True)
        user.refresh_from_db()
        self.assertEqual(user.is_verified, False)
        self.assertEqual(user.verified_by, None)

        # Login
        self.force_login(moderator)

        content = _query_check()['data']['moderatorMutation']['userVerify']['result']
        self.assertEqual(content['isVerified'], True)
        user.refresh_from_db()
        self.assertEqual(user.is_verified, True)
        self.assertEqual(user.verified_by, moderator)

    @override_settings(
        MAX_LOGIN_ATTEMPTS=1,
        MAX_CAPTCHA_LOGIN_ATTEMPTS=2,
    )
    @mock.patch('apps.user.serializers.validate_hcaptcha')
    def test_too_many_logins_needs_captcha_and_more_will_throttle(self, validate):
        User._reset_login_cache(self.user.email)
        validate.return_value = False
        self.query_check(
            self.login_mutation,
            minput={'email': self.user.email, 'password': self.user.password_text},
            okay=True
        )

        # attempt 1
        self.query_check(
            self.login_mutation,
            minput={'email': self.user.email, 'password': 'wrong_password'},
            okay=False
        )

        # attempt 2
        self.query_check(
            self.login_mutation,
            minput={'email': self.user.email, 'password': 'wrong_password'},
            okay=False
        )

        # attempt 3
        # try again and it should fail with captcha error
        content = self.query_check(
            self.login_mutation,
            minput={'email': self.user.email, 'password': 'wrong_password'},
            okay=False
        )
        self.assertFalse(content['data']['login']['ok'])
        self.assertTrue(content['data']['login']['captchaRequired'])

        # attempt 4
        # invalid password and invalid captcha should raise invalid captcha
        content = self.query_check(
            self.login_mutation,
            input_data={
                'email': self.user.email,
                'password': 'wrong_password',
                'captcha': 'wrong=kaj',
                'siteKey': 'fffffff',
            },
            okay=False
        )
        self.assertFalse(content['data']['login']['ok'])
        self.assertTrue(content['data']['login']['captchaRequired'])
        self.assertIn('the captcha is invalid.', content['data']['login']['errors'][0]['messages'].lower())

    @override_settings(
        MAX_LOGIN_ATTEMPTS=1
    )
    @mock.patch('apps.user.serializers.validate_hcaptcha')
    def test_too_many_logins_with_valid_captcha(self, validate):
        User._reset_login_cache(self.user.email)
        self.query_check(
            self.login_mutation,
            input_data={'email': self.user.email, 'password': self.user.password_text},
            okay=True
        )

        # attempt 1
        self.query_check(
            self.login_mutation,
            input_data={'email': self.user.email, 'password': 'worng'},
            okay=False
        )

        # attempt 2
        # try again and it should fail with captcha error
        self.query_check(
            self.login_mutation,
            input_data={'email': self.user.email, 'password': 'wrong'},
            okay=False
        )

        # again with captcha but wrong
        validate.return_value = False
        content = self.query_check(
            self.login_mutation,
            input_data={
                'email': self.user.email,
                'password': self.user.password_text,
                'captcha': 'random',
                'siteKey': 'random',
            },
            okay=False
        )
        self.assertTrue(content['data']['login']['captchaRequired'])
        self.assertIn('the captcha is invalid.', content['data']['login']['errors'][0]['messages'].lower())

        # with correct captcha
        validate.return_value = True
        self.query_check(
            self.login_mutation,
            input_data={
                'email': self.user.email,
                'password': self.user.password_text,
                'captcha': 'aa',
                'siteKey': 'aa',
            },
            okay=True
        )
