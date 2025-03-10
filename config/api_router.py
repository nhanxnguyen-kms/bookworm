from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from bookworm.catalog.api.views import BookViewSet, CategoryViewSet
from bookworm.user.api.views import UserViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()


router.register("catalog/categories", CategoryViewSet, basename="categories")
router.register("catalog/books", BookViewSet, basename="books")
router.register("users", UserViewSet, basename="users")


urlpatterns = router.urls
