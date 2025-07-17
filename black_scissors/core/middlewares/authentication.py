from graphql_jwt.middleware import JSONWebTokenMiddleware

class CustomJWTAuthMiddleware(JSONWebTokenMiddleware):
    def resolve(self, next, root, info, **kwargs):
        request = info.context
        auth_header = request.META.get("HTTP_AUTHORIZATION", "")

        if auth_header.startswith("Bearer "):
            # Convert Bearer token to JWT token format
            token = auth_header.split(" ")[1]
            request.META["HTTP_AUTHORIZATION"] = f"JWT {token}"

        return super().resolve(next, root, info, **kwargs)