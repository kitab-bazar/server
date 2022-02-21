from utils.graphene.tests import GraphQLTestCase

from config.permissions import UserPermissions

from apps.user.models import User
from apps.book.models import Book

from apps.user.factories import UserFactory
from apps.publisher.factories import PublisherFactory
from apps.book.factories import AuthorFactory, CategoryFactory, BookFactory
from apps.common.factories import MunicipalityFactory
from apps.school.factories import SchoolFactory
from apps.institution.factories import InstitutionFactory


class TestPermissions(GraphQLTestCase):
    def setUp(self):
        self.individual_user = UserFactory.create(user_type=User.UserType.INSTITUTIONAL_USER.value)
        self.publisher_user = UserFactory.create(user_type=User.UserType.PUBLISHER.value)
        self.school_admin_user = UserFactory.create(user_type=User.UserType.SCHOOL_ADMIN.value)
        self.institutional_user = UserFactory.create(user_type=User.UserType.INSTITUTIONAL_USER.value)
        self.super_admin = UserFactory.create(user_type=User.UserType.MODERATOR.value)
        super().setUp()


class TestBookPermissions(TestPermissions):
    def setUp(self):
        self.create_book = '''
            mutation Mutation($input: BookCreateInputType!) {
                createBook(data: $input) {
                    ok
                    errors
                    result {
                      id
                      title
                    }
                }
            }
        '''

        self.update_book = '''
            mutation Mutation($id: ID!, $input: BookCreateInputType!) {
                updateBook(id: $id data: $input) {
                    ok
                    errors
                    result {
                      id
                      title
                    }
                }
            }
        '''

        self.delete_book = '''
            mutation Mutation($id: ID!) {
                deleteBook(id: $id) {
                    ok
                    errors
                }
            }
        '''
        author = AuthorFactory.create()
        category = CategoryFactory.create()
        self.book_publisher = PublisherFactory.create()
        self.minput = {
            'title': "book title", 'isbn': "123456789", 'numberOfPages': 10,
            'language': Book.LanguageType.NEPALI.name, 'publishedDate': "2018-01-01",
            'edition': "1", 'price': 10, 'publisher': self.book_publisher.id,
            'authors': [author.id], 'categories': [category.id],
            'isPublished': True
        }
        self.book = BookFactory.create(publisher=self.book_publisher)
        super().setUp()

    def test_admin_and_publisher_only_can_create_book(self):
        # Admin case
        self.force_login(self.super_admin)
        content = self.query_check(self.create_book, minput=self.minput, okay=True)
        self.assertEqual(content['data']['createBook']['result']['title'], self.minput['title'])

        # Publisher case
        self.publisher_user.publisher = self.book_publisher
        self.publisher_user.save()
        self.force_login(self.publisher_user)
        self.query_check(self.create_book, minput=self.minput, okay=True)
        self.assertEqual(content['data']['createBook']['result']['title'], self.minput['title'])

        # School admin case
        self.force_login(self.school_admin_user)
        response = self.query_check(self.create_book, minput=self.minput, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_CREATE_BOOK)
        )

        # Institution case
        self.force_login(self.institutional_user)
        response = self.query_check(self.create_book, minput=self.minput, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_CREATE_BOOK)
        )

        # Individual user case
        self.force_login(self.individual_user)
        response = self.query_check(self.create_book, minput=self.minput, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_CREATE_BOOK)
        )

    def test_admin_and_publisher_only_can_update_book(self):
        # Admin case
        updated_title = 'updated book title'
        self.minput['title'] = updated_title

        self.force_login(self.super_admin)
        content = self.query_check(
            self.update_book, minput=self.minput,
            variables={'id': self.book.id}, okay=True
        )
        self.assertEqual(content['data']['updateBook']['result']['title'], updated_title)

        # Publisher case
        updated_title = 'updated book title latest'
        self.minput['title'] = updated_title
        self.publisher_user.publisher = self.book_publisher
        self.publisher_user.save()
        self.force_login(self.publisher_user)
        content = self.query_check(
            self.update_book, minput=self.minput,
            variables={'id': self.book.id}, okay=True
        )
        self.assertEqual(content['data']['updateBook']['result']['title'], updated_title)

        # School admin case
        self.force_login(self.school_admin_user)
        response = self.query_check(
            self.update_book, minput=self.minput, variables={'id': self.book.id},
            assert_for_error=True
        )
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_UPDATE_BOOK)
        )

        # Institution case
        self.force_login(self.institutional_user)
        response = self.query_check(
            self.update_book, minput=self.minput, variables={'id': self.book.id},
            assert_for_error=True
        )
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_UPDATE_BOOK)
        )

        # Individual user case
        self.force_login(self.individual_user)
        response = self.query_check(
            self.update_book, minput=self.minput, variables={'id': self.book.id},
            assert_for_error=True
        )
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_UPDATE_BOOK)
        )

    def test_admin_and_publisher_only_can_delete_book(self):
        # Admin case
        self.force_login(self.super_admin)
        book = BookFactory.create(publisher=self.book_publisher)
        self.query_check(self.delete_book, variables={'id': book.id}, okay=True)

        # Publisher case
        self.force_login(self.publisher_user)
        self.publisher_user.publisher = self.book_publisher
        self.publisher_user.save()
        book = BookFactory.create(publisher=self.book_publisher)
        self.query_check(self.delete_book, variables={'id': book.id}, okay=True)

        # School admin case
        self.force_login(self.school_admin_user)
        response = self.query_check(self.delete_book, variables={'id': book.id}, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_DELETE_BOOK)
        )

        # Institution case
        self.force_login(self.institutional_user)
        response = self.query_check(self.delete_book, variables={'id': book.id}, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_DELETE_BOOK)
        )

        # Individual user case
        self.force_login(self.individual_user)
        response = self.query_check(self.delete_book, variables={'id': book.id}, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_DELETE_BOOK)
        )


class TestPublisherPermissions(TestPermissions):
    def setUp(self):
        self.create_publisher = '''
            mutation Mutation($input: PublisherCreateInputType!) {
                createPublisher(data: $input) {
                    ok
                    errors
                    result {
                      id
                      name
                    }
                }
            }
        '''

        self.update_publisher = '''
            mutation Mutation($id: ID!, $input: PublisherCreateInputType!) {
                updatePublisher(id: $id data: $input) {
                    ok
                    errors
                    result {
                      id
                      name
                    }
                }
            }
        '''

        self.delete_publisher = '''
            mutation Mutation($id: ID!) {
                deletePublisher(id: $id) {
                    ok
                    errors
                }
            }
        '''
        municipality = MunicipalityFactory.create()
        self.publisher_minput = {
            'localAddress': "Kathmandu", 'municipality': municipality.id,
            'name': "Ekta Books", 'panNumber': "1324322",
            'vatNumber': "2342FD45", 'wardNumber': 10
        }
        self.book_publisher = PublisherFactory.create()
        super().setUp()

    def test_admin_only_can_create_publisher(self):
        # Admin case
        self.force_login(self.super_admin)
        content = self.query_check(self.create_publisher, minput=self.publisher_minput, okay=True)
        self.assertEqual(content['data']['createPublisher']['result']['name'], self.publisher_minput['name'])

        # Publisher case
        self.publisher_user.publisher = self.book_publisher
        self.publisher_user.save()
        self.force_login(self.publisher_user)
        response = self.query_check(self.create_publisher, minput=self.publisher_minput, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_CREATE_PUBLISHER)
        )
        # School admin case
        self.force_login(self.school_admin_user)
        response = self.query_check(self.create_publisher, minput=self.publisher_minput, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_CREATE_PUBLISHER)
        )

        # Institution case
        self.force_login(self.institutional_user)
        response = self.query_check(self.create_publisher, minput=self.publisher_minput, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_CREATE_PUBLISHER)
        )

        # Individual user case
        self.force_login(self.individual_user)
        response = self.query_check(self.create_publisher, minput=self.publisher_minput, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_CREATE_PUBLISHER)
        )

    def test_admin_only_can_update_publishers(self):
        publisher = PublisherFactory.create()

        # Admin case
        updated_name = 'updated publisher name'
        self.publisher_minput['name'] = updated_name

        self.force_login(self.super_admin)
        content = self.query_check(
            self.update_publisher, minput=self.publisher_minput,
            variables={'id': publisher.id}, okay=True
        )
        self.assertEqual(content['data']['updatePublisher']['result']['name'], updated_name)

        # Publisher case
        self.force_login(self.publisher_user)
        response = self.query_check(
            self.update_publisher, minput=self.publisher_minput, variables={'id': publisher.id},
            assert_for_error=True
        )
        # Object level permission
        self.assertEqual(
            response['errors'][0]['message'],
            'Publisher matching query does not exist.'
        )

        # School admin case
        self.force_login(self.school_admin_user)
        response = self.query_check(
            self.update_publisher, minput=self.publisher_minput, variables={'id': publisher.id},
            assert_for_error=True
        )
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_UPDATE_PUBLISHER)
        )

        # Institution case
        self.force_login(self.institutional_user)
        response = self.query_check(
            self.update_publisher, minput=self.publisher_minput, variables={'id': publisher.id},
            assert_for_error=True
        )
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_UPDATE_PUBLISHER)
        )

        # Individual user case
        self.force_login(self.individual_user)
        response = self.query_check(
            self.update_publisher, minput=self.publisher_minput, variables={'id': publisher.id},
            assert_for_error=True
        )
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_UPDATE_PUBLISHER)
        )

    def test_publisher_can_update_his_profile(self):
        publisher = PublisherFactory.create()
        # Set user profile to publisher
        self.publisher_user.publisher = publisher
        self.publisher_user.save()

        self.force_login(self.publisher_user)
        updated_name = 'Manakamana books'
        self.publisher_minput['name'] = updated_name
        content = self.query_check(
            self.update_publisher, minput=self.publisher_minput,
            variables={'id': publisher.id}, okay=True
        )
        self.assertEqual(content['data']['updatePublisher']['result']['name'], updated_name)

    def test_admin_only_can_delete_publisher(self):
        # Admin case
        self.force_login(self.super_admin)
        publisher = PublisherFactory.create()
        self.query_check(self.delete_publisher, variables={'id': publisher.id}, okay=True)

        # Publisher case
        self.force_login(self.publisher_user)
        publisher = PublisherFactory.create()
        self.publisher_user.publisher = publisher
        self.publisher_user.save()
        response = self.query_check(self.delete_publisher, variables={'id': publisher.id}, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_DELETE_PUBLISHER)
        )
        # School admin case
        self.force_login(self.school_admin_user)
        response = self.query_check(self.delete_publisher, variables={'id': publisher.id}, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_DELETE_PUBLISHER)
        )

        # Institution case
        self.force_login(self.institutional_user)
        response = self.query_check(self.delete_publisher, variables={'id': publisher.id}, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_DELETE_PUBLISHER)
        )

        # Individual user case
        self.force_login(self.individual_user)
        response = self.query_check(self.delete_publisher, variables={'id': publisher.id}, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_DELETE_PUBLISHER)
        )


class TestSchoolPermissions(TestPermissions):
    def setUp(self):
        self.create_school = '''
            mutation Mutation($input: SchoolCreateInputType!) {
                createSchool(data: $input) {
                    ok
                    errors
                    result {
                      id
                      name
                    }
                }
            }
        '''

        self.update_school = '''
            mutation Mutation($id: ID!, $input: SchoolCreateInputType!) {
                updateSchool(id: $id data: $input) {
                    ok
                    errors
                    result {
                      id
                      name
                    }
                }
            }
        '''

        self.delete_school = '''
            mutation Mutation($id: ID!) {
                deleteSchool(id: $id) {
                    ok
                    errors
                }
            }
        '''
        self.municipality = MunicipalityFactory.create()
        self.school_minput = {
            'localAddress': "Kanchanpur", 'municipality': self.municipality.id,
            'name': "Radiant secondary school", 'panNumber': "556633232",
            'vatNumber': "233E333", 'wardNumber': 3
        }
        self.school = SchoolFactory.create()
        super().setUp()

    def test_admin_only_can_create_school(self):
        # Admin case
        self.force_login(self.super_admin)
        content = self.query_check(self.create_school, minput=self.school_minput, okay=True)
        self.assertEqual(content['data']['createSchool']['result']['name'], self.school_minput['name'])

        # Set school admin user profile to school
        self.school_admin_user.school = self.school
        self.school_admin_user.save()

        # Publisher case
        self.force_login(self.publisher_user)
        response = self.query_check(self.create_school, minput=self.school_minput, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_CREATE_SCHOOL)
        )
        # School admin case
        self.force_login(self.school_admin_user)
        response = self.query_check(self.create_school, minput=self.school_minput, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_CREATE_SCHOOL)
        )

        # Institution case
        self.force_login(self.institutional_user)
        response = self.query_check(self.create_school, minput=self.school_minput, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_CREATE_SCHOOL)
        )

        # Individual user case
        self.force_login(self.individual_user)
        response = self.query_check(self.create_school, minput=self.school_minput, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_CREATE_SCHOOL)
        )

    def test_admin_only_can_update_schools(self):
        school = SchoolFactory.create()

        # Admin case
        updated_name = 'Udaya Dev secondary school'
        self.school_minput['name'] = updated_name

        self.force_login(self.super_admin)
        content = self.query_check(
            self.update_school, minput=self.school_minput,
            variables={'id': school.id}, okay=True
        )
        self.assertEqual(content['data']['updateSchool']['result']['name'], updated_name)

        # Publisher case
        self.force_login(self.publisher_user)
        response = self.query_check(
            self.update_school, minput=self.school_minput, variables={'id': school.id},
            assert_for_error=True
        )
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_UPDATE_SCHOOL)
        )

        # School admin case
        self.force_login(self.school_admin_user)
        response = self.query_check(
            self.update_school, minput=self.school_minput, variables={'id': school.id},
            assert_for_error=True
        )
        # Object level permission
        self.assertEqual(
            response['errors'][0]['message'],
            'School matching query does not exist.'
        )

        # Institution case
        self.force_login(self.institutional_user)
        response = self.query_check(
            self.update_school, minput=self.school_minput, variables={'id': school.id},
            assert_for_error=True
        )
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_UPDATE_SCHOOL)
        )

        # Individual user case
        self.force_login(self.individual_user)
        response = self.query_check(
            self.update_school, minput=self.school_minput, variables={'id': school.id},
            assert_for_error=True
        )
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_UPDATE_SCHOOL)
        )

    def test_school_can_update_his_profile(self):
        school = SchoolFactory.create()
        updated_name = 'Pashupati primary school'
        self.school_minput['name'] = updated_name

        # Set school admin user profile to school
        self.school_admin_user.school = school
        self.school_admin_user.save()

        self.force_login(self.school_admin_user)
        content = self.query_check(
            self.update_school, minput=self.school_minput,
            variables={'id': school.id}, okay=True
        )
        self.assertEqual(content['data']['updateSchool']['result']['name'], updated_name)

    def test_admin_only_can_delete_school(self):
        # Admin case
        self.force_login(self.super_admin)
        school = SchoolFactory.create()
        self.query_check(self.delete_school, variables={'id': school.id}, okay=True)

        # Publisher case
        self.force_login(self.publisher_user)
        school = SchoolFactory.create()
        self.publisher_user.school = school
        self.publisher_user.save()
        response = self.query_check(self.delete_school, variables={'id': school.id}, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_DELETE_SCHOOL)
        )
        # School admin case
        self.force_login(self.school_admin_user)
        response = self.query_check(self.delete_school, variables={'id': school.id}, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_DELETE_SCHOOL)
        )

        # Institution case
        self.force_login(self.institutional_user)
        response = self.query_check(self.delete_school, variables={'id': school.id}, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_DELETE_SCHOOL)
        )

        # Individual user case
        self.force_login(self.individual_user)
        response = self.query_check(self.delete_school, variables={'id': school.id}, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_DELETE_SCHOOL)
        )


class TestInstitutionPermissions(TestPermissions):
    def setUp(self):
        self.create_institution = '''
            mutation Mutation($input: InstitutionCreateInputType!) {
                createInstitution(data: $input) {
                    ok
                    errors
                    result {
                      id
                      name
                    }
                }
            }
        '''

        self.update_institution = '''
            mutation Mutation($id: ID!, $input: InstitutionCreateInputType!) {
                updateInstitution(id: $id data: $input) {
                    ok
                    errors
                    result {
                      id
                      name
                    }
                }
            }
        '''

        self.delete_institution = '''
            mutation Mutation($id: ID!) {
                deleteInstitution(id: $id) {
                    ok
                    errors
                }
            }
        '''
        self.municipality = MunicipalityFactory.create()
        self.institution_minput = {
            'localAddress': "Kailali", 'municipality': self.municipality.id,
            'name': "XYZ institution", 'panNumber': "349EE34999",
            'vatNumber': "777777777V", 'wardNumber': 20
        }
        self.institution = InstitutionFactory.create()
        super().setUp()

    def test_admin_only_can_create_institution(self):
        # Admin case
        self.force_login(self.super_admin)
        content = self.query_check(self.create_institution, minput=self.institution_minput, okay=True)
        self.assertEqual(content['data']['createInstitution']['result']['name'], self.institution_minput['name'])

        # Set school admin user profile to school
        self.institutional_user.institution = self.institution
        self.institutional_user.save()

        # Publisher case
        self.force_login(self.publisher_user)
        response = self.query_check(self.create_institution, minput=self.institution_minput, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_CREATE_INSTITUTION)
        )
        # School admin case
        self.force_login(self.school_admin_user)
        response = self.query_check(self.create_institution, minput=self.institution_minput, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_CREATE_INSTITUTION)
        )

        # Institution case
        self.force_login(self.institutional_user)
        response = self.query_check(self.create_institution, minput=self.institution_minput, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_CREATE_INSTITUTION)
        )

        # Individual user case
        self.force_login(self.individual_user)
        response = self.query_check(self.create_institution, minput=self.institution_minput, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_CREATE_INSTITUTION)
        )

    def test_admin_only_can_update_institutions(self):
        institution = InstitutionFactory.create()
        # Admin case
        updated_name = 'ABC institution'
        self.institution_minput['name'] = updated_name

        self.force_login(self.super_admin)
        content = self.query_check(
            self.update_institution, minput=self.institution_minput,
            variables={'id': institution.id}, okay=True
        )
        self.assertEqual(content['data']['updateInstitution']['result']['name'], updated_name)

        # Publisher case
        self.force_login(self.publisher_user)
        response = self.query_check(
            self.update_institution, minput=self.institution_minput, variables={'id': institution.id},
            assert_for_error=True
        )
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_UPDATE_INSTITUTION)
        )

        # School admin case
        self.force_login(self.school_admin_user)
        response = self.query_check(
            self.update_institution, minput=self.institution_minput, variables={'id': institution.id},
            assert_for_error=True
        )
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_UPDATE_INSTITUTION)
        )

        # Institutional user case
        self.force_login(self.institutional_user)
        response = self.query_check(
            self.update_institution, minput=self.institution_minput, variables={'id': institution.id},
            assert_for_error=True
        )
        self.assertEqual(
            response['errors'][0]['message'],
            'Institution matching query does not exist.'
        )

        # Individual user case
        self.force_login(self.individual_user)
        # FIXME: Find how user type changed
        self.individual_user.user_type = User.UserType.INDIVIDUAL_USER.value
        self.individual_user.save()
        response = self.query_check(
            self.update_institution, minput=self.institution_minput, variables={'id': institution.id},
            assert_for_error=True
        )
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_UPDATE_INSTITUTION)
        )

    def test_institution_can_update_his_profile(self):
        pass

    def test_admin_only_can_delete_institution(self):
        # Admin case
        self.force_login(self.super_admin)
        institution = InstitutionFactory.create()
        self.query_check(self.delete_institution, variables={'id': institution.id}, okay=True)

        # Publisher case
        institution = InstitutionFactory.create()
        self.force_login(self.publisher_user)
        response = self.query_check(self.delete_institution, variables={'id': institution.id}, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_DELETE_INSTITUTION)
        )
        # School admin case
        self.force_login(self.school_admin_user)
        response = self.query_check(self.delete_institution, variables={'id': institution.id}, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_DELETE_INSTITUTION)
        )

        # Institution case
        self.force_login(self.institutional_user)
        self.institutional_user.institution = institution
        self.institutional_user.save()
        response = self.query_check(self.delete_institution, variables={'id': institution.id}, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_DELETE_INSTITUTION)
        )

        # Individual user case
        self.force_login(self.individual_user)
        response = self.query_check(self.delete_institution, variables={'id': institution.id}, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_DELETE_INSTITUTION)
        )
