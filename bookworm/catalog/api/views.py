import logging

from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets

from bookworm.catalog.api.serializers import BookSerializer, CategorySerializer
from bookworm.catalog.models import Book, Category

logger = logging.getLogger(__name__)


@extend_schema(tags=["Category"])
class CategoryViewSet(viewsets.ModelViewSet):
    """
    A view-set for viewing and editing category instances.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


@extend_schema(tags=["Book"])
class BookViewSet(viewsets.ModelViewSet):
    """
    A view-set for viewing and editing book instances.
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend]
    search_fields = ["name"]
