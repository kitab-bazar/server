import graphene
from graphene_django import DjangoObjectType
from graphene_django_extras import DjangoObjectField, PageGraphqlPagination

from utils.graphene.types import CustomDjangoListObjectType, FileFieldType
from utils.graphene.fields import DjangoPaginatedListObjectField

from apps.blog.models import Blog, Tag, Category
from apps.blog.filters import BlogFilter, TagFilter, CategoryFilter


class BlogTagType(DjangoObjectType):
    class Meta:
        model = Tag
        fields = (
            'id', 'name'
        )


class BlogTagListType(CustomDjangoListObjectType):
    class Meta:
        model = Tag
        filterset_class = TagFilter


class BlogCategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = (
            'id', 'name', 'parent_category'
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
            'id', 'title', 'description', 'image', 'category', 'tags', 'published_date',
            'meta_title', 'meta_keywords', 'meta_description', 'og_title',
            'og_description', 'og_image', 'og_locale', 'og_type',
        )

    image = graphene.Field(FileFieldType)
    og_image = graphene.Field(FileFieldType)


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
