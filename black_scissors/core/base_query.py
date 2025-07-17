import graphene
from graphql import GraphQLError
from graphql_relay import from_global_id


class BaseQuery(graphene.ObjectType):

    class Meta:
        abstract = True


    @classmethod
    def handle_query(cls, request):
        return True

    @classmethod
    def get_id(cls, model_id=None):
        if model_id is not None:
            return from_global_id(model_id)[1]
        return None