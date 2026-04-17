from django.urls import path
from users.views import CreateUserView, ManageUserView, LogoutUserView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

app_name = "users"

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("logout/", LogoutUserView.as_view(), name="logout"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token-verify"),
    path("me/", ManageUserView.as_view(), name="manage-user"),
]
