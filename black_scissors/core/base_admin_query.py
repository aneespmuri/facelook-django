import graphene
from graphql import GraphQLError
from graphql_relay import from_global_id


class BaseAdminQuery(graphene.ObjectType):
    authentication_required = True

    class Meta:
        abstract = True

    @classmethod
    def handle_admin_query(cls, request):
        if cls.authentication_required and not request.user.is_authenticated:
            raise GraphQLError('Invalid Token.')
        return True

    @classmethod
    def get_id(cls, model_id=None):
        if model_id is not None:
            return from_global_id(model_id)[1]
        return None
