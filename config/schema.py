import graphene
from apps.user import schema as user_schema, mutations as user_mutations


# schemas
class Query(
    user_schema.Query,
    graphene.ObjectType,
):
    pass


# mutations
class Mutation(
    user_mutations.Mutation,
    graphene.ObjectType
):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
