from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from newhire.users.api.views import UserViewSet
from newhire.blog.api.views import PostViewSet, CategoryViewSet, CommentViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("posts", PostViewSet)
router.register("categories", CategoryViewSet)
router.register("comments", CommentViewSet)
router.register("users", UserViewSet)


app_name = "api"
urlpatterns = router.urls
