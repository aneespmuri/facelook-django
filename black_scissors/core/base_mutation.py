import graphene
from graphene import relay
from graphql import GraphQLError
from graphql_relay import from_global_id


class BaseMutation(relay.ClientIDMutation):
    # errors = ErrorType()
    message = graphene.String()
    status_code = graphene.Int()
    # authentication_required = True

    class Meta:
        abstract = True

    @classmethod
    def handle_mutation(cls, request):
        return True

    @classmethod
    def get_id(cls, model_id=None):
        if model_id is not None:
            return from_global_id(model_id)[1]
        return None
