from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication


class ApiAuthMixin:
    authentication_classes = (SessionAuthentication, )
    permission_classes = (IsAuthenticated, )

