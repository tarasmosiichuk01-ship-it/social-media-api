from django.urls import path
from users.views import (
    RegisterUserView,
    ManageProfileUserView,
    LogoutUserView,
    UserListView,
    UserProfileView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

app_name = "users"

urlpatterns = [
    path("users/", UserListView.as_view(), name="user-list"),
    path("users/<int:pk>/", UserProfileView.as_view(), name="user-detail"),
    path("register/", RegisterUserView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("logout/", LogoutUserView.as_view(), name="logout"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token-verify"),
    path("me/", ManageProfileUserView.as_view(), name="manage-user"),
]
