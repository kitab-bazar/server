import io
import json
from unittest import mock
from PIL import Image

from django.core.files.storage import FileSystemStorage
from utils.graphene.tests import GraphQLTestCase

from apps.user.models import User
from apps.blog.factories import BlogFactory, BlogCategoryFactory
from apps.user.factories import UserFactory
from apps.book.factories import BookFactory
from apps.publisher.factories import PublisherFactory


class TestOgFileUpload(GraphQLTestCase):
    def generate_image_file(self):
        file = io.BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        return file

    def setUp(self):
        self.create_blog = '''
            mutation Mutation($input:  BlogInputType!) {
                createBlog(data: $input) {
                    ok
                    errors
                    result {
                       id
                       image {
                         name
                         url
                       }
                       ogImage {
                         name
                         url
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
                       image {
                         name
                         url
                       }
                       ogImage {
                         name
                         url
                       }
                    }
                }
            }
        '''
        self.create_book = '''
            mutation Mutation($input:  BookCreateInputType!) {
                createBook(data: $input) {
                    ok
                    errors
                    result {
                       id
                       image {
                         name
                         url
                       }
                       ogImage {
                         name
                         url
                       }
                    }
                }
            }
        '''
        self.update_book = '''
            mutation Mutation($id: ID!, $input:  BookCreateInputType!) {
                updateBook(id: $id data: $input) {
                    ok
                    errors
                    result {
                       id
                       image {
                         name
                         url
                       }
                       ogImage {
                         name
                         url
                       }
                    }
                }
            }
        '''
        # Blog setup
        blog_category = BlogCategoryFactory.create()
        blog = BlogFactory.create(category=blog_category)
        self.create_blog_variables = {
            'input': {
                'publishedDate': '2000-01-01', 'category': blog_category.id,
                'image': None,
            }
        }
        self.update_blog_variables = dict(self.create_blog_variables, **{'id': blog.id})

        # Book setup
        book_publisher = PublisherFactory.create()
        book = BookFactory.create(publisher=book_publisher)
        self.create_book_variables = {
            'input': {
                'publishedDate': '2000-01-01', 'image': None,
            }
        }
        self.update_book_variables = dict(self.create_book_variables, **{'id': book.id})

        self.admin = UserFactory.create(user_type=User.UserType.ADMIN.value)
        super().setUp()

    def check_image_upload_asserts(self, query, variables):
        self.force_login(self.admin)
        image_file = self.generate_image_file()
        response = self._client.post(
            '/graphql/',
            data={
                'operations': json.dumps({
                    'query': self.update_blog,
                    'variables': self.update_blog_variables,
                }),
                'image': image_file,
                'map': json.dumps({
                    'image': ['variables.input.image']
                })
            }
        )
        content = response.json()
        self.assertTrue(content['data']['updateBlog']['ok'], content)
        self.assertTrue(content['data']['updateBlog']['result']['image'])
        image_name = content['data']['updateBlog']['result']['image']['name']
        self.assertTrue(image_name.endswith('.png'))
        self.assertTrue(content['data']['updateBlog']['result']['ogImage'])
        og_image_name = content['data']['updateBlog']['result']['ogImage']['name']
        self.assertTrue(og_image_name.endswith('.png'))

    @mock.patch('storages.backends.s3boto3.S3StaticStorage', FileSystemStorage)
    def test_can_create_blog_image_in_s3_static_storage(self):
        self.check_image_upload_asserts(self.update_blog, self.update_blog_variables)

    @mock.patch('storages.backends.s3boto3.S3StaticStorage', FileSystemStorage)
    def test_can_update_blog_image_in_s3_static_storage(self):
        self.check_image_upload_asserts(self.create_blog, self.create_blog_variables)

    @mock.patch('storages.backends.s3boto3.S3StaticStorage', FileSystemStorage)
    def test_can_create_book_image_in_s3_static_storage(self):
        self.check_image_upload_asserts(self.update_book, self.update_book_variables)

    @mock.patch('storages.backends.s3boto3.S3StaticStorage', FileSystemStorage)
    def test_can_update_book_image_in_s3_static_storage(self):
        self.check_image_upload_asserts(self.create_book, self.create_book_variables)
