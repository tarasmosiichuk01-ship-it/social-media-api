from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import (
    UserProfileSerializer,
    LogoutSerializer,
    UserListSerializer,
    UserDetailSerializer,
)


class RegisterUserView(generics.CreateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = ()


class LogoutUserView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class ManageProfileUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class UserProfileView(generics.RetrieveAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = (IsAuthenticated,)


class UserListView(generics.ListAPIView):
    serializer_class = UserListSerializer

    def get_queryset(self):
        queryset = get_user_model().objects.all()
        username = self.request.GET.get("username")

        if username:
            queryset = queryset.filter(username__icontains=username)

        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "username",
                type=str,
                description="Filter by username",
                required=False,
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        """Get list of users"""
        return super().list(request, *args, **kwargs)


class FollowUnfollowView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        target_user = get_object_or_404(get_user_model(), id=pk)

        if request.user == target_user:
            return Response(
                {"detail": "Cannot follow yourself"}, status=status.HTTP_400_BAD_REQUEST
            )

        if request.user.following.filter(id=target_user.id).exists():
            request.user.following.remove(target_user)
            return Response({"detail": "Unfollowed"}, status=status.HTTP_200_OK)

        request.user.following.add(target_user)
        return Response({"detail": "Followed"}, status=status.HTTP_200_OK)


class FollowingListView(generics.ListAPIView):
    serializer_class = UserListSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        following = self.request.user.following.all()
        return following


class FollowersListView(generics.ListAPIView):
    serializer_class = UserListSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        followers = self.request.user.followers.all()
        return followers
