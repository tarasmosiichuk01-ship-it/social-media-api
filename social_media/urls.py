from django.urls import path, include
from rest_framework import routers

from social_media.views import PostViewSet, CommentViewSet

app_name = "social_media"

router = routers.DefaultRouter()
router.register("posts", PostViewSet)
posts_router = routers.NestedDefaultRouter(router, "posts", lookup="post")
posts_router.register("comments", CommentViewSet, basename="post-comments")

urlpatterns = [
    path("", include(router.urls)),
]
