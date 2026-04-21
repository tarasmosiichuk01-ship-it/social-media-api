from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, permissions
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.decorators import action
from rest_framework.response import Response
from social_media.models import Post, Like, Comment
from social_media.permissions import IsAuthorOrReadOnly
from social_media.serializers import (
    PostSerializer,
    PostListSerializer,
    CommentSerializer,
)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    permission_classes = (IsAuthorOrReadOnly,)

    def get_queryset(self):
        queryset = self.queryset

        user = self.request.user
        following_users = user.following.values_list("following", flat=True)

        if self.action == "list":
            queryset = (
                Post.objects.filter(author__in=following_users)
                .select_related("author")
                .prefetch_related("likes", "hashtags", "comments")
            )
            return queryset

        hashtag = self.request.query_params.get("hashtag")
        author = self.request.query_params.get("author")

        if hashtag:
            queryset = queryset.filter(hashtags__name__iexact=hashtag)
        if author:
            queryset = queryset.filter(author__id=author.id)

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return PostListSerializer
        return PostSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["post"], url_path="like")
    def like(self, request, pk=None):
        post = self.get_object()
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if not created:
            like.delete()
            return Response({"liked": False}, status=status.HTTP_200_OK)

        return Response({"liked": True}, status=status.HTTP_201_CREATED)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "author",
                type={"type": "array", "items": {"type": "number"}},
                description="Filter by author id ex. ?airplane_types=2,3",
                required=False,
                explode=False,
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        """Get list of posts"""
        return super().list(request, *args, **kwargs)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs["post_pk"]).select_related(
            "author"
        )

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs["post_pk"])
        serializer.save(author=self.request.user, post=post)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "authors",
                type={"type": "array", "items": {"type": "number"}},
                description="Filter by author id ex. ?authors=2,3",
                required=False,
                explode=False,
            ),
            OpenApiParameter(
                "posts",
                type={"type": "array", "items": {"type": "number"}},
                description="Filter by posts id ex. ?posts=2,3",
                required=False,
                explode=False,
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        """Get list of comments"""
        return super().list(request, *args, **kwargs)
