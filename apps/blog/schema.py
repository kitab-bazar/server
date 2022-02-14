import graphene
from graphene_django import DjangoObjectType
from graphene_django_extras import DjangoObjectField, PageGraphqlPagination

from django.db.models import QuerySet

from utils.graphene.types import CustomDjangoListObjectType, FileFieldType
from utils.graphene.fields import DjangoPaginatedListObjectField

from apps.blog.models import Blog, Tag, Category
from apps.blog.filters import BlogFilter, TagFilter, CategoryFilter


def get_blog_qs(info):
    return Blog.objects.filter(blog_publish_type=Blog.BlogPublishType.PUBLISH)


class BlogTagType(DjangoObjectType):
    class Meta:
        model = Tag
        fields = (
            'id', 'name', 'name_en', 'name_ne'
        )


class BlogTagListType(CustomDjangoListObjectType):
    class Meta:
        model = Tag
        filterset_class = TagFilter


class BlogCategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = (
            'id', 'name', 'name_en', 'name_ne'
        )


class BlogCategoryListType(CustomDjangoListObjectType):
    class Meta:
        model = Category
        filterset_class = CategoryFilter


class BlogType(DjangoObjectType):
    quantity_in_cart = graphene.Int(required=True)

    class Meta:
        model = Blog
        fields = (
            # model fields
            'id', 'image', 'og_image', 'category', 'tags', 'published_date',
            'blog_publish_type', 'title', 'description', 'meta_title', 'meta_keywords',
            'meta_description', 'og_title', 'og_description', 'og_locale', 'og_type',

            # English fields
            'title_en', 'description_en', 'meta_title_en', 'meta_keywords_en',
            'meta_description_en', 'og_title_en', 'og_description_en', 'og_locale_en',
            'og_type_en',

            # Nepali fields
            'title_ne', 'description_ne', 'meta_title_ne', 'meta_keywords_ne',
            'meta_description_ne', 'og_title_ne', 'og_description_ne', 'og_locale_ne', 'og_type_ne',
        )

    image = graphene.Field(FileFieldType)
    og_image = graphene.Field(FileFieldType)

    @staticmethod
    def get_custom_queryset(queryset, info):
        return get_blog_qs(info)


class BlogListType(CustomDjangoListObjectType):
    class Meta:
        model = Blog
        filterset_class = BlogFilter


class Query(graphene.ObjectType):
    blog = DjangoObjectField(BlogType)
    blogs = DjangoPaginatedListObjectField(
        BlogListType,
        pagination=PageGraphqlPagination(
            page_size_query_param='pageSize'
        )
    )
    blog_categories = DjangoPaginatedListObjectField(
        BlogCategoryListType,
        pagination=PageGraphqlPagination(
            page_size_query_param='pageSize'
        )
    )
    blog_tags = DjangoPaginatedListObjectField(
        BlogTagListType,
        pagination=PageGraphqlPagination(
            page_size_query_param='pageSize'
        )
    )

    @staticmethod
    def resolve_blogs(root, info, **kwargs) -> QuerySet:
        return get_blog_qs(info)
