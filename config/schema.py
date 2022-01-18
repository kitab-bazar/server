import graphene

from apps.user import schema as user_schema, mutations as user_mutations
from apps.common import schema as common_schema
from apps.institution import schema as institution_schema, mutations as institution_mutations
from apps.publisher import schema as publisher_schema, mutations as publisher_mutations
from apps.school import schema as school_schema, mutations as school_mutations
from apps.book import schema as book_schema, mutations as book_mutations
from apps.order import schema as order_schema, mutations as order_mutations


# schemas
class Query(
    user_schema.Query,
    common_schema.Query,
    institution_schema.Query,
    publisher_schema.Query,
    school_schema.Query,
    book_schema.Query,
    order_schema.Query,
    graphene.ObjectType,
):
    pass


# mutations
class Mutation(
    user_mutations.Mutation,
    institution_mutations.Mutation,
    publisher_mutations.Mutation,
    school_mutations.Mutation,
    book_mutations.Mutation,
    order_mutations.Mutation,
    graphene.ObjectType,
):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
