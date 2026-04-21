from django.urls import path, include
from rest_framework import routers
from rest_framework_nested import routers as nested_routers

from social_media.views import PostViewSet, CommentViewSet

app_name = "social_media"

router = routers.DefaultRouter()
router.register("posts", PostViewSet, basename="post")
posts_router = nested_routers.NestedDefaultRouter(router, "posts", lookup="post")
posts_router.register("comments", CommentViewSet, basename="post-comments")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(posts_router.urls)),
]
