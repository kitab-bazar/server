import graphene
from .graphene_converter import *  # type: ignore # noqa F401

from apps.user import schema as user_schema, mutations as user_mutations
from apps.common import schema as common_schema, mutations as common_mutations
from apps.institution import schema as institution_schema, mutations as institution_mutations
from apps.publisher import schema as publisher_schema, mutations as publisher_mutations
from apps.school import schema as school_schema, mutations as school_mutations
from apps.book import schema as book_schema, mutations as book_mutations
from apps.order import schema as order_schema, mutations as order_mutations
from apps.notification import schema as notification_schema, mutations as notification_mutations
from apps.helpdesk import schema as helpdesk_schema, mutations as helpdesk_mutations
from apps.blog import schema as blog_schema, mutations as blog_mutations
from apps.package import schema as package_schema


# schemas
class Query(
    user_schema.Query,
    common_schema.Query,
    institution_schema.Query,
    publisher_schema.Query,
    school_schema.Query,
    book_schema.Query,
    notification_schema.Query,
    order_schema.Query,
    helpdesk_schema.Query,
    blog_schema.Query,
    package_schema.Query,
    graphene.ObjectType,
):
    pass


# mutations
class Mutation(
    user_mutations.Mutation,
    common_mutations.Mutation,
    institution_mutations.Mutation,
    publisher_mutations.Mutation,
    school_mutations.Mutation,
    book_mutations.Mutation,
    order_mutations.Mutation,
    notification_mutations.Mutation,
    helpdesk_mutations.Mutation,
    blog_mutations.Mutation,
    graphene.ObjectType,
):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
