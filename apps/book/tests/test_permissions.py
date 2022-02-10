from apps.common.tests.test_permissions import TestPermissions
from config.permissions import UserPermissions

from apps.book.factories import CategoryFactory, TagFactory, AuthorFactory


class TestBookCategoryPermissions(TestPermissions):
    def setUp(self):
        super(TestBookCategoryPermissions, self).setUp()
        self.create_book_category = '''
            mutation Mutation($input: BookCategoryInputType!) {
                createBookCategory(data: $input) {
                    ok
                    errors
                    result {
                      id
                      name
                    }
                }
            }
        '''
        self.update_book_category = '''
            mutation Mutation($id: ID!, $input:  BookCategoryInputType!) {
                updateBookCategory(id: $id data: $input) {
                    ok
                    errors
                    result {
                      id
                      name
                    }
                }
            }
        '''
        self.delete_book_category = '''
            mutation Mutation($id: ID!) {
                deleteBookCategory(id: $id) {
                    ok
                    errors
                }
            }
        '''
        self.book_category_minput = {
            'name': 'Test category'
        }
        super().setUp()

    def test_admin_only_can_create_book_category(self):
        # Admin case
        self.force_login(self.super_admin)
        content = self.query_check(self.create_book_category, minput=self.book_category_minput, okay=True)
        self.assertEqual(content['data']['createBookCategory']['result']['name'], self.book_category_minput['name'])

        # Publisher case
        self.force_login(self.publisher_user)
        response = self.query_check(self.create_book_category, minput=self.book_category_minput, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_CREATE_BOOK_CATEGORY)
        )

        # School admin case
        self.force_login(self.school_admin_user)
        response = self.query_check(self.create_book_category, minput=self.book_category_minput, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_CREATE_BOOK_CATEGORY)
        )

        # Institution case
        self.force_login(self.institutional_user)
        response = self.query_check(self.create_book_category, minput=self.book_category_minput, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_CREATE_BOOK_CATEGORY)
        )

        # Individual user case
        self.force_login(self.individual_user)
        response = self.query_check(self.create_book_category, minput=self.book_category_minput, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_CREATE_BOOK_CATEGORY)
        )

    def test_admin_only_can_update_book_categorys(self):
        book_category = CategoryFactory.create()

        # Admin case
        updated_name = 'updated name'
        self.book_category_minput['name'] = updated_name

        self.force_login(self.super_admin)
        content = self.query_check(
            self.update_book_category, minput=self.book_category_minput,
            variables={'id': book_category.id}, okay=True
        )
        self.assertEqual(content['data']['updateBookCategory']['result']['name'], self.book_category_minput['name'])

        # Publisher case
        self.force_login(self.publisher_user)
        response = self.query_check(
            self.update_book_category, minput=self.book_category_minput, variables={'id': book_category.id},
            assert_for_error=True
        )
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_UPDATE_BOOK_CATEGORY)
        )

        # School admin case
        self.force_login(self.school_admin_user)
        response = self.query_check(
            self.update_book_category, minput=self.book_category_minput, variables={'id': book_category.id},
            assert_for_error=True
        )
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_UPDATE_BOOK_CATEGORY)
        )

        # Institution case
        self.force_login(self.institutional_user)
        response = self.query_check(
            self.update_book_category, minput=self.book_category_minput, variables={'id': book_category.id},
            assert_for_error=True
        )
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_UPDATE_BOOK_CATEGORY)
        )

        # Individual user case
        self.force_login(self.individual_user)
        response = self.query_check(
            self.update_book_category, minput=self.book_category_minput, variables={'id': book_category.id},
            assert_for_error=True
        )
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_UPDATE_BOOK_CATEGORY)
        )

    def test_admin_only_can_delete_book_category(self):
        # Admin case
        self.force_login(self.super_admin)
        book_category = CategoryFactory.create()
        self.query_check(self.delete_book_category, variables={'id': book_category.id}, okay=True)

        book_category = CategoryFactory.create()

        # Publisher case
        self.force_login(self.publisher_user)
        response = self.query_check(self.delete_book_category, variables={'id': book_category.id}, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_DELETE_BOOK_CATEGORY)
        )

        # School admin case
        self.force_login(self.school_admin_user)
        response = self.query_check(self.delete_book_category, variables={'id': book_category.id}, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_DELETE_BOOK_CATEGORY)
        )

        # Institution case
        self.force_login(self.institutional_user)
        response = self.query_check(self.delete_book_category, variables={'id': book_category.id}, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_DELETE_BOOK_CATEGORY)
        )

        # Individual user case
        self.force_login(self.individual_user)
        response = self.query_check(self.delete_book_category, variables={'id': book_category.id}, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_DELETE_BOOK_CATEGORY)
        )


class TestBookTagPermissions(TestPermissions):
    def setUp(self):
        super(TestBookTagPermissions, self).setUp()
        self.create_book_tag = '''
            mutation Mutation($input: BookTagInputType!) {
                createBookTag(data: $input) {
                    ok
                    errors
                    result {
                      id
                      name
                    }
                }
            }
        '''
        self.update_book_tag = '''
            mutation Mutation($id: ID!, $input:  BookTagInputType!) {
                updateBookTag(id: $id data: $input) {
                    ok
                    errors
                    result {
                      id
                      name
                    }
                }
            }
        '''
        self.delete_book_tag = '''
            mutation Mutation($id: ID!) {
                deleteBookTag(id: $id) {
                    ok
                    errors
                }
            }
        '''
        self.book_tag_minput = {
            'name': 'Test category'
        }
        super().setUp()

    def test_admin_only_can_create_book_tag(self):
        # Admin case
        self.force_login(self.super_admin)
        content = self.query_check(self.create_book_tag, minput=self.book_tag_minput, okay=True)
        self.assertEqual(content['data']['createBookTag']['result']['name'], self.book_tag_minput['name'])

        # Publisher case
        self.force_login(self.publisher_user)
        response = self.query_check(self.create_book_tag, minput=self.book_tag_minput, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_CREATE_BOOK_TAG)
        )

        # School admin case
        self.force_login(self.school_admin_user)
        response = self.query_check(self.create_book_tag, minput=self.book_tag_minput, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_CREATE_BOOK_TAG)
        )

        # Institution case
        self.force_login(self.institutional_user)
        response = self.query_check(self.create_book_tag, minput=self.book_tag_minput, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_CREATE_BOOK_TAG)
        )

        # Individual user case
        self.force_login(self.individual_user)
        response = self.query_check(self.create_book_tag, minput=self.book_tag_minput, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_CREATE_BOOK_TAG)
        )

    def test_admin_only_can_update_book_tags(self):
        book_tag = TagFactory.create()

        # Admin case
        updated_name = 'updated name'
        self.book_tag_minput['name'] = updated_name

        self.force_login(self.super_admin)
        content = self.query_check(
            self.update_book_tag, minput=self.book_tag_minput,
            variables={'id': book_tag.id}, okay=True
        )
        self.assertEqual(content['data']['updateBookTag']['result']['name'], self.book_tag_minput['name'])

        # Publisher case
        self.force_login(self.publisher_user)
        response = self.query_check(
            self.update_book_tag, minput=self.book_tag_minput, variables={'id': book_tag.id},
            assert_for_error=True
        )
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_UPDATE_BOOK_TAG)
        )

        # School admin case
        self.force_login(self.school_admin_user)
        response = self.query_check(
            self.update_book_tag, minput=self.book_tag_minput, variables={'id': book_tag.id},
            assert_for_error=True
        )
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_UPDATE_BOOK_TAG)
        )

        # Institution case
        self.force_login(self.institutional_user)
        response = self.query_check(
            self.update_book_tag, minput=self.book_tag_minput, variables={'id': book_tag.id},
            assert_for_error=True
        )
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_UPDATE_BOOK_TAG)
        )

        # Individual user case
        self.force_login(self.individual_user)
        response = self.query_check(
            self.update_book_tag, minput=self.book_tag_minput, variables={'id': book_tag.id},
            assert_for_error=True
        )
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_UPDATE_BOOK_TAG)
        )

    def test_admin_only_can_delete_book_tag(self):
        # Admin case
        self.force_login(self.super_admin)
        book_tag = TagFactory.create()
        self.query_check(self.delete_book_tag, variables={'id': book_tag.id}, okay=True)

        book_tag = TagFactory.create()

        # Publisher case
        self.force_login(self.publisher_user)
        response = self.query_check(self.delete_book_tag, variables={'id': book_tag.id}, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_DELETE_BOOK_TAG)
        )

        # School admin case
        self.force_login(self.school_admin_user)
        response = self.query_check(self.delete_book_tag, variables={'id': book_tag.id}, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_DELETE_BOOK_TAG)
        )

        # Institution case
        self.force_login(self.institutional_user)
        response = self.query_check(self.delete_book_tag, variables={'id': book_tag.id}, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_DELETE_BOOK_TAG)
        )

        # Individual user case
        self.force_login(self.individual_user)
        response = self.query_check(self.delete_book_tag, variables={'id': book_tag.id}, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_DELETE_BOOK_TAG)
        )


class TestBookAuthorPermissions(TestPermissions):
    def setUp(self):
        super(TestBookAuthorPermissions, self).setUp()
        self.create_book_author = '''
            mutation Mutation($input: BookAuthorInputType!) {
                createBookAuthor(data: $input) {
                    ok
                    errors
                    result {
                      id
                      name
                    }
                }
            }
        '''
        self.update_book_author = '''
            mutation Mutation($id: ID!, $input:  BookAuthorInputType!) {
                updateBookAuthor(id: $id data: $input) {
                    ok
                    errors
                    result {
                      id
                      name
                    }
                }
            }
        '''
        self.delete_book_author = '''
            mutation Mutation($id: ID!) {
                deleteBookAuthor(id: $id) {
                    ok
                    errors
                }
            }
        '''
        self.book_author_minput = {
            'name': 'Test category'
        }
        super().setUp()

    def test_admin_and_publisher_only_can_create_book_author(self):
        # Admin case
        self.force_login(self.super_admin)
        content = self.query_check(self.create_book_author, minput=self.book_author_minput, okay=True)
        self.assertEqual(content['data']['createBookAuthor']['result']['name'], self.book_author_minput['name'])

        # Publisher case
        self.force_login(self.publisher_user)
        content = self.query_check(self.create_book_author, minput=self.book_author_minput, okay=True)
        self.assertEqual(content['data']['createBookAuthor']['result']['name'], self.book_author_minput['name'])

        # School admin case
        self.force_login(self.school_admin_user)
        response = self.query_check(self.create_book_author, minput=self.book_author_minput, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_CREATE_BOOK_AUTHOR)
        )

        # Institution case
        self.force_login(self.institutional_user)
        response = self.query_check(self.create_book_author, minput=self.book_author_minput, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_CREATE_BOOK_AUTHOR)
        )

        # Individual user case
        self.force_login(self.individual_user)
        response = self.query_check(self.create_book_author, minput=self.book_author_minput, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_CREATE_BOOK_AUTHOR)
        )

    def test_admin_and_publisher_only_can_update_book_authors(self):
        book_author = AuthorFactory.create()

        # Admin case
        updated_name = 'updated name'
        self.book_author_minput['name'] = updated_name

        self.force_login(self.super_admin)
        content = self.query_check(
            self.update_book_author, minput=self.book_author_minput,
            variables={'id': book_author.id}, okay=True
        )
        self.assertEqual(content['data']['updateBookAuthor']['result']['name'], self.book_author_minput['name'])

        # Publisher case
        self.force_login(self.publisher_user)
        content = self.query_check(
            self.update_book_author, minput=self.book_author_minput,
            variables={'id': book_author.id}, okay=True
        )
        self.assertEqual(content['data']['updateBookAuthor']['result']['name'], self.book_author_minput['name'])

        # School admin case
        self.force_login(self.school_admin_user)
        response = self.query_check(
            self.update_book_author, minput=self.book_author_minput, variables={'id': book_author.id},
            assert_for_error=True
        )
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_UPDATE_BOOK_AUTHOR)
        )

        # Institution case
        self.force_login(self.institutional_user)
        response = self.query_check(
            self.update_book_author, minput=self.book_author_minput, variables={'id': book_author.id},
            assert_for_error=True
        )
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_UPDATE_BOOK_AUTHOR)
        )

        # Individual user case
        self.force_login(self.individual_user)
        response = self.query_check(
            self.update_book_author, minput=self.book_author_minput, variables={'id': book_author.id},
            assert_for_error=True
        )
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_UPDATE_BOOK_AUTHOR)
        )

    def test_admin_only_can_delete_book_author(self):
        # Admin case
        self.force_login(self.super_admin)
        book_author = AuthorFactory.create()
        self.query_check(self.delete_book_author, variables={'id': book_author.id}, okay=True)

        book_author = AuthorFactory.create()

        # Publisher case
        self.force_login(self.publisher_user)
        response = self.query_check(self.delete_book_author, variables={'id': book_author.id}, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_DELETE_BOOK_AUTHOR)
        )

        # School admin case
        self.force_login(self.school_admin_user)
        response = self.query_check(self.delete_book_author, variables={'id': book_author.id}, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_DELETE_BOOK_AUTHOR)
        )

        # Institution case
        self.force_login(self.institutional_user)
        response = self.query_check(self.delete_book_author, variables={'id': book_author.id}, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_DELETE_BOOK_AUTHOR)
        )

        # Individual user case
        self.force_login(self.individual_user)
        response = self.query_check(self.delete_book_author, variables={'id': book_author.id}, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_DELETE_BOOK_AUTHOR)
        )
