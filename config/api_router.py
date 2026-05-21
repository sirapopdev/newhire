from rest_framework.routers import DefaultRouter, SimpleRouter

from django.conf import settings

from newhire.users.api.views import UserViewSet
from newhire.api.views import PostViewSet, CategoryViewSet, CommentViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("posts", PostViewSet)
router.register("categories", CategoryViewSet)
router.register("comments", CommentViewSet)
router.register("users", UserViewSet)


app_name = "api"
urlpatterns = router.urls
