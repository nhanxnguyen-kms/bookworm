import logging

from drf_spectacular.utils import extend_schema
from knox.views import LoginView as KnoxLoginView
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import action
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from bookworm.user.api.serializers import UserSerializer
from bookworm.user.models import User

logger = logging.getLogger(__name__)


@extend_schema(tags=["User"])
class UserViewSet(
    RetrieveModelMixin,
    ListModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    GenericViewSet,
):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self) -> User:
        return User.objects.filter(id=self.request.user.id)

    def get_permissions(self) -> list:
        if self.action == "create":
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=["get"])
    def me(self, request) -> Response:
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )

        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        user = User.objects.create_user(**data)

        return Response(UserSerializer(user).data, status=201)

    @action(detail=True, methods=["delete"])
    def delete(self, pk=None) -> Response:
        user = self.get_object()
        user.delete()
        return Response(status=204)


@extend_schema(tags=["Authentication"])
class LoginView(KnoxLoginView):
    authentication_classes = [BasicAuthentication]
