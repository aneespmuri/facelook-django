import graphene

from scissors.graphql.schema import ScissorMutation, ScissorsQuery


class Mutation(ScissorMutation, ):
    pass


class Query(ScissorsQuery, ):
    pass


schema = graphene.Schema(mutation=Mutation, query=Query)
