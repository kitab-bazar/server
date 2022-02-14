from apps.common.tests.test_permissions import TestPermissions
from config.permissions import UserPermissions

from apps.blog.models import Blog
from apps.blog.factories import BlogFactory, BlogCategoryFactory, BlogTagFactory


class TestBlogPermissions(TestPermissions):
    def setUp(self):
        super(TestBlogPermissions, self).setUp()
        self.create_blog = '''
            mutation Mutation($input: BlogInputType!) {
                createBlog(data: $input) {
                    ok
                    errors
                    result {
                      id
                      title
                      description
                      category {
                        id
                      }
                    }
                }
            }
        '''
        self.update_blog = '''
            mutation Mutation($id: ID!, $input:  BlogInputType!) {
                updateBlog(id: $id data: $input) {
                    ok
                    errors
                    result {
                      id
                       title
                       description
                       category {
                         id
                       }
                    }
                }
            }
        '''
        self.delete_blog = '''
            mutation Mutation($id: ID!) {
                deleteBlog(id: $id) {
                    ok
                    errors
                }
            }
        '''
        self.blog_category = BlogCategoryFactory.create()
        self.blog = BlogFactory.create(category=self.blog_category)
        self.blog_minput = {
            'titleEn': 'Test title', 'descriptionEn': 'Test description',
            'publishedDate': '2021-09-12', 'category': self.blog_category.id,
            'blogPublishType': Blog.BlogPublishType.DRAFT.name
        }

        super().setUp()

    def test_admin_only_can_create_blog(self):
        # Admin case
        self.force_login(self.super_admin)
        content = self.query_check(self.create_blog, minput=self.blog_minput, okay=True)
        self.assertEqual(content['data']['createBlog']['result']['title'], self.blog_minput['titleEn'])
        self.assertEqual(content['data']['createBlog']['result']['description'], self.blog_minput['descriptionEn'])
        self.assertEqual(content['data']['createBlog']['result']['category']['id'], str(self.blog_minput['category']))

        # Publisher case
        self.force_login(self.publisher_user)
        response = self.query_check(self.create_blog, minput=self.blog_minput, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_CREATE_BLOG)
        )

        # School admin case
        self.force_login(self.school_admin_user)
        response = self.query_check(self.create_blog, minput=self.blog_minput, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_CREATE_BLOG)
        )

        # Institution case
        self.force_login(self.institutional_user)
        response = self.query_check(self.create_blog, minput=self.blog_minput, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_CREATE_BLOG)
        )

        # Individual user case
        self.force_login(self.individual_user)
        response = self.query_check(self.create_blog, minput=self.blog_minput, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_CREATE_BLOG)
        )

    def test_admin_only_can_update_blogs(self):
        blog = BlogFactory.create()

        # Admin case
        updated_title = 'updated title'
        self.blog_minput['titleEn'] = updated_title

        self.force_login(self.super_admin)
        content = self.query_check(
            self.update_blog, minput=self.blog_minput,
            variables={'id': blog.id}, okay=True
        )
        self.assertEqual(content['data']['updateBlog']['result']['title'], self.blog_minput['titleEn'])
        self.assertEqual(content['data']['updateBlog']['result']['description'], self.blog_minput['descriptionEn'])
        self.assertEqual(content['data']['updateBlog']['result']['category']['id'], str(self.blog_minput['category']))

        # Publisher case
        self.force_login(self.publisher_user)
        response = self.query_check(
            self.update_blog, minput=self.blog_minput, variables={'id': blog.id},
            assert_for_error=True
        )
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_UPDATE_BLOG)
        )

        # School admin case
        self.force_login(self.school_admin_user)
        response = self.query_check(
            self.update_blog, minput=self.blog_minput, variables={'id': blog.id},
            assert_for_error=True
        )
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_UPDATE_BLOG)
        )

        # Institution case
        self.force_login(self.institutional_user)
        response = self.query_check(
            self.update_blog, minput=self.blog_minput, variables={'id': blog.id},
            assert_for_error=True
        )
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_UPDATE_BLOG)
        )

        # Individual user case
        self.force_login(self.individual_user)
        response = self.query_check(
            self.update_blog, minput=self.blog_minput, variables={'id': blog.id},
            assert_for_error=True
        )
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_UPDATE_BLOG)
        )

    def test_admin_only_can_delete_blog(self):
        # Admin case
        self.force_login(self.super_admin)
        blog = BlogFactory.create()
        self.query_check(self.delete_blog, variables={'id': blog.id}, okay=True)

        blog = BlogFactory.create()

        # Publisher case
        self.force_login(self.publisher_user)
        response = self.query_check(self.delete_blog, variables={'id': blog.id}, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_DELETE_BLOG)
        )

        # School admin case
        self.force_login(self.school_admin_user)
        response = self.query_check(self.delete_blog, variables={'id': blog.id}, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_DELETE_BLOG)
        )

        # Institution case
        self.force_login(self.institutional_user)
        response = self.query_check(self.delete_blog, variables={'id': blog.id}, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_DELETE_BLOG)
        )

        # Individual user case
        self.force_login(self.individual_user)
        response = self.query_check(self.delete_blog, variables={'id': blog.id}, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_DELETE_BLOG)
        )


class TestBlogCategoryPermissions(TestPermissions):
    def setUp(self):
        super(TestBlogCategoryPermissions, self).setUp()
        self.create_blog_category = '''
            mutation Mutation($input: BlogCategoryInputType!) {
                createBlogCategory(data: $input) {
                    ok
                    errors
                    result {
                      id
                      name
                    }
                }
            }
        '''
        self.update_blog_category = '''
            mutation Mutation($id: ID!, $input:  BlogCategoryInputType!) {
                updateBlogCategory(id: $id data: $input) {
                    ok
                    errors
                    result {
                      id
                      name
                    }
                }
            }
        '''
        self.delete_blog_category = '''
            mutation Mutation($id: ID!) {
                deleteBlogCategory(id: $id) {
                    ok
                    errors
                }
            }
        '''
        self.blog_category_minput = {
            'nameEn': 'Test category'
        }
        super().setUp()

    def test_admin_only_can_create_blog_category(self):
        # Admin case
        self.force_login(self.super_admin)
        content = self.query_check(self.create_blog_category, minput=self.blog_category_minput, okay=True)
        self.assertEqual(content['data']['createBlogCategory']['result']['name'], self.blog_category_minput['nameEn'])

        # Publisher case
        self.force_login(self.publisher_user)
        response = self.query_check(self.create_blog_category, minput=self.blog_category_minput, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_CREATE_BLOG_CATEGORY)
        )

        # School admin case
        self.force_login(self.school_admin_user)
        response = self.query_check(self.create_blog_category, minput=self.blog_category_minput, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_CREATE_BLOG_CATEGORY)
        )

        # Institution case
        self.force_login(self.institutional_user)
        response = self.query_check(self.create_blog_category, minput=self.blog_category_minput, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_CREATE_BLOG_CATEGORY)
        )

        # Individual user case
        self.force_login(self.individual_user)
        response = self.query_check(self.create_blog_category, minput=self.blog_category_minput, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_CREATE_BLOG_CATEGORY)
        )

    def test_admin_only_can_update_blog_categorys(self):
        blog_category = BlogCategoryFactory.create()

        # Admin case
        updated_name = 'updated name'
        self.blog_category_minput['nameEn'] = updated_name

        self.force_login(self.super_admin)
        content = self.query_check(
            self.update_blog_category, minput=self.blog_category_minput,
            variables={'id': blog_category.id}, okay=True
        )
        self.assertEqual(content['data']['updateBlogCategory']['result']['name'], self.blog_category_minput['nameEn'])

        # Publisher case
        self.force_login(self.publisher_user)
        response = self.query_check(
            self.update_blog_category, minput=self.blog_category_minput, variables={'id': blog_category.id},
            assert_for_error=True
        )
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_UPDATE_BLOG_CATEGORY)
        )

        # School admin case
        self.force_login(self.school_admin_user)
        response = self.query_check(
            self.update_blog_category, minput=self.blog_category_minput, variables={'id': blog_category.id},
            assert_for_error=True
        )
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_UPDATE_BLOG_CATEGORY)
        )

        # Institution case
        self.force_login(self.institutional_user)
        response = self.query_check(
            self.update_blog_category, minput=self.blog_category_minput, variables={'id': blog_category.id},
            assert_for_error=True
        )
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_UPDATE_BLOG_CATEGORY)
        )

        # Individual user case
        self.force_login(self.individual_user)
        response = self.query_check(
            self.update_blog_category, minput=self.blog_category_minput, variables={'id': blog_category.id},
            assert_for_error=True
        )
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_UPDATE_BLOG_CATEGORY)
        )

    def test_admin_only_can_delete_blog_category(self):
        # Admin case
        self.force_login(self.super_admin)
        blog_category = BlogCategoryFactory.create()
        self.query_check(self.delete_blog_category, variables={'id': blog_category.id}, okay=True)

        blog_category = BlogCategoryFactory.create()

        # Publisher case
        self.force_login(self.publisher_user)
        response = self.query_check(self.delete_blog_category, variables={'id': blog_category.id}, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_DELETE_BLOG_CATEGORY)
        )

        # School admin case
        self.force_login(self.school_admin_user)
        response = self.query_check(self.delete_blog_category, variables={'id': blog_category.id}, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_DELETE_BLOG_CATEGORY)
        )

        # Institution case
        self.force_login(self.institutional_user)
        response = self.query_check(self.delete_blog_category, variables={'id': blog_category.id}, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_DELETE_BLOG_CATEGORY)
        )

        # Individual user case
        self.force_login(self.individual_user)
        response = self.query_check(self.delete_blog_category, variables={'id': blog_category.id}, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_DELETE_BLOG_CATEGORY)
        )


class TestBlogTagPermissions(TestPermissions):
    def setUp(self):
        super(TestBlogTagPermissions, self).setUp()
        self.create_blog_tag = '''
            mutation Mutation($input: BlogTagInputType!) {
                createBlogTag(data: $input) {
                    ok
                    errors
                    result {
                      id
                      name
                    }
                }
            }
        '''
        self.update_blog_tag = '''
            mutation Mutation($id: ID!, $input:  BlogTagInputType!) {
                updateBlogTag(id: $id data: $input) {
                    ok
                    errors
                    result {
                      id
                      name
                    }
                }
            }
        '''
        self.delete_blog_tag = '''
            mutation Mutation($id: ID!) {
                deleteBlogTag(id: $id) {
                    ok
                    errors
                }
            }
        '''
        self.blog_tag_minput = {
            'nameEn': 'Test tag'
        }
        super().setUp()

    def test_admin_only_can_create_blog_tag(self):
        # Admin case
        self.force_login(self.super_admin)
        content = self.query_check(self.create_blog_tag, minput=self.blog_tag_minput, okay=True)
        self.assertEqual(content['data']['createBlogTag']['result']['name'], self.blog_tag_minput['nameEn'])

        # Publisher case
        self.force_login(self.publisher_user)
        response = self.query_check(self.create_blog_tag, minput=self.blog_tag_minput, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_CREATE_BLOG_TAG)
        )

        # School admin case
        self.force_login(self.school_admin_user)
        response = self.query_check(self.create_blog_tag, minput=self.blog_tag_minput, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_CREATE_BLOG_TAG)
        )

        # Institution case
        self.force_login(self.institutional_user)
        response = self.query_check(self.create_blog_tag, minput=self.blog_tag_minput, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_CREATE_BLOG_TAG)
        )

        # Individual user case
        self.force_login(self.individual_user)
        response = self.query_check(self.create_blog_tag, minput=self.blog_tag_minput, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_CREATE_BLOG_TAG)
        )

    def test_admin_only_can_update_blog_tags(self):
        blog_tag = BlogTagFactory.create()

        # Admin case
        updated_name = 'updated name'
        self.blog_tag_minput['nameEn'] = updated_name

        self.force_login(self.super_admin)
        content = self.query_check(
            self.update_blog_tag, minput=self.blog_tag_minput,
            variables={'id': blog_tag.id}, okay=True
        )
        self.assertEqual(content['data']['updateBlogTag']['result']['name'], self.blog_tag_minput['nameEn'])

        # Publisher case
        self.force_login(self.publisher_user)
        response = self.query_check(
            self.update_blog_tag, minput=self.blog_tag_minput, variables={'id': blog_tag.id},
            assert_for_error=True
        )
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_UPDATE_BLOG_TAG)
        )

        # School admin case
        self.force_login(self.school_admin_user)
        response = self.query_check(
            self.update_blog_tag, minput=self.blog_tag_minput, variables={'id': blog_tag.id},
            assert_for_error=True
        )
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_UPDATE_BLOG_TAG)
        )

        # Institution case
        self.force_login(self.institutional_user)
        response = self.query_check(
            self.update_blog_tag, minput=self.blog_tag_minput, variables={'id': blog_tag.id},
            assert_for_error=True
        )
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_UPDATE_BLOG_TAG)
        )

        # Individual user case
        self.force_login(self.individual_user)
        response = self.query_check(
            self.update_blog_tag, minput=self.blog_tag_minput, variables={'id': blog_tag.id},
            assert_for_error=True
        )
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_UPDATE_BLOG_TAG)
        )

    def test_admin_only_can_delete_blog_tag(self):
        # Admin case
        self.force_login(self.super_admin)
        blog_tag = BlogTagFactory.create()
        self.query_check(self.delete_blog_tag, variables={'id': blog_tag.id}, okay=True)

        blog_tag = BlogTagFactory.create()

        # Publisher case
        self.force_login(self.publisher_user)
        response = self.query_check(self.delete_blog_tag, variables={'id': blog_tag.id}, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_DELETE_BLOG_TAG)
        )

        # School admin case
        self.force_login(self.school_admin_user)
        response = self.query_check(self.delete_blog_tag, variables={'id': blog_tag.id}, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_DELETE_BLOG_TAG)
        )

        # Institution case
        self.force_login(self.institutional_user)
        response = self.query_check(self.delete_blog_tag, variables={'id': blog_tag.id}, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_DELETE_BLOG_TAG)
        )

        # Individual user case
        self.force_login(self.individual_user)
        response = self.query_check(self.delete_blog_tag, variables={'id': blog_tag.id}, assert_for_error=True)
        self.assertEqual(
            response['errors'][0]['message'],
            UserPermissions.get_permission_message(UserPermissions.Permission.CAN_DELETE_BLOG_TAG)
        )
