from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from users.apps import UsersConfig
from users.serializers import CustomTokenObtainPairSerializer
from users.views import LogoutView, RegisterView, UserProfileView

app_name = UsersConfig.name

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),  # регистрация
    path("logout/", LogoutView.as_view(), name="logout"),
    path(
        "token/",
        TokenObtainPairView.as_view(serializer_class=CustomTokenObtainPairSerializer),
        name="token_obtain_pair",
    ),  # login/вход
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path(
        "profile/", UserProfileView.as_view(), name="profile"
    ),  # редактирование профиля
]
