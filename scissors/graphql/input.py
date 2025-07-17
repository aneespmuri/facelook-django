import graphene


class DetailInput(graphene.InputObjectType):
    first_name = graphene.String(required=True)
    last_name = graphene.String(required=True)
    email = graphene.String(required=True)
    phone_no = graphene.String(required=True)
    notes = graphene.String()
