import graphene
from utils.graphene.mutation import (
    generate_input_type_for_serializer,
    CreateUpdateGrapheneMutation,
    DeleteMutation
)

from apps.user.models import User
from apps.blog.models import Blog, Category, Tag
from apps.blog.schema import BlogType, BlogCategoryType, BlogTagType
from apps.blog.serializers import BlogSerializer, BlogCategorySerializer, BlogTagSerializer
from config.permissions import UserPermissions


BlogInputType = generate_input_type_for_serializer(
    'BlogInputType',
    serializer_class=BlogSerializer
)


class BaseBlogMutationMixin():
    @classmethod
    def filter_queryset(cls, qs, info):
        if info.context.user.user_type == User.UserType.ADMIN.value:
            return qs
        return qs.none()


class CreateBlog(BaseBlogMutationMixin, CreateUpdateGrapheneMutation):
    class Arguments:
        data = BlogInputType(required=True)
    model = Blog
    serializer_class = BlogSerializer
    result = graphene.Field(BlogType)
    permissions = [UserPermissions.Permission.CAN_CREATE_BLOG]


class UpdateBlog(BaseBlogMutationMixin, CreateUpdateGrapheneMutation):
    class Arguments:
        data = BlogInputType(required=True)
        id = graphene.ID(required=True)
    model = Blog
    serializer_class = BlogSerializer
    result = graphene.Field(BlogType)
    permissions = [UserPermissions.Permission.CAN_UPDATE_BLOG]


class DeleteBlog(BaseBlogMutationMixin, DeleteMutation):
    class Arguments:
        id = graphene.ID(required=True)
    model = Blog
    result = graphene.Field(BlogType)
    permissions = [UserPermissions.Permission.CAN_DELETE_BLOG]


BlogTagInputType = generate_input_type_for_serializer(
    'BlogTagInputType',
    serializer_class=BlogTagSerializer
)


class CreateBlogTag(BaseBlogMutationMixin, CreateUpdateGrapheneMutation):
    class Arguments:
        data = BlogTagInputType(required=True)
    model = Tag
    serializer_class = BlogTagSerializer
    result = graphene.Field(BlogTagType)
    permissions = [UserPermissions.Permission.CAN_CREATE_BLOG_TAG]


class UpdateBlogTag(BaseBlogMutationMixin, CreateUpdateGrapheneMutation):
    class Arguments:
        data = BlogTagInputType(required=True)
        id = graphene.ID(required=True)
    model = Tag
    serializer_class = BlogTagSerializer
    result = graphene.Field(BlogTagType)
    permissions = [UserPermissions.Permission.CAN_UPDATE_BLOG_TAG]


class DeleteBlogTag(BaseBlogMutationMixin, DeleteMutation):
    class Arguments:
        id = graphene.ID(required=True)
    model = Tag
    result = graphene.Field(BlogTagType)
    permissions = [UserPermissions.Permission.CAN_DELETE_BLOG_TAG]


BlogCategoryInputType = generate_input_type_for_serializer(
    'BlogCategoryInputType',
    serializer_class=BlogCategorySerializer
)


class CreateBlogCategory(BaseBlogMutationMixin, CreateUpdateGrapheneMutation):
    class Arguments:
        data = BlogCategoryInputType(required=True)
    model = Category
    serializer_class = BlogCategorySerializer
    result = graphene.Field(BlogCategoryType)
    permissions = [UserPermissions.Permission.CAN_CREATE_BLOG_CATEGORY]


class UpdateBlogCategory(BaseBlogMutationMixin, CreateUpdateGrapheneMutation):
    class Arguments:
        data = BlogCategoryInputType(required=True)
        id = graphene.ID(required=True)
    model = Category
    serializer_class = BlogCategorySerializer
    result = graphene.Field(BlogCategoryType)
    permissions = [UserPermissions.Permission.CAN_UPDATE_BLOG_CATEGORY]


class DeleteBlogCategory(BaseBlogMutationMixin, DeleteMutation):
    class Arguments:
        id = graphene.ID(required=True)
    model = Category
    result = graphene.Field(BlogCategoryType)
    permissions = [UserPermissions.Permission.CAN_DELETE_BLOG_CATEGORY]


class Mutation(graphene.ObjectType):
    create_blog = CreateBlog.Field()
    update_blog = UpdateBlog.Field()
    delete_blog = DeleteBlog.Field()
    create_blog_tag = CreateBlogTag.Field()
    update_blog_tag = UpdateBlogTag.Field()
    delete_blog_tag = DeleteBlogTag.Field()
    create_blog_category = CreateBlogCategory.Field()
    update_blog_category = UpdateBlogCategory.Field()
    delete_blog_category = DeleteBlogCategory.Field()
