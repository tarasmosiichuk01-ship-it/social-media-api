from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status, generics, viewsets, filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from users.serializers import (
    UserProfileSerializer,
    LogoutSerializer,
    UserRegistrationSerializer,
    UserListSerializer,
    UserDetailSerializer,
)


class RegisterUserView(generics.CreateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = ()


class LoginUserView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    serializer_class = UserRegistrationSerializer


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
    serializer_class = UserProfileSerializer


class UserListView(generics.ListAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserListSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["username", "email"]

    def get_queryset(self):
        queryset = self.queryset
        username = self.request.GET.get("username")

        if username:
            queryset = queryset.filter(username__icontains=username)

        return queryset


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
