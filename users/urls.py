from django.urls import include, path
from rest_framework.permissions import AllowAny
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenRefreshView

from users.apps import UsersConfig
# from users.views import (MyTokenObtainPairView, PaymentAPIView, PaymentViewSet,
#                          UserCreateAPIView, UserProfileView)

app_name = UsersConfig.name

router = SimpleRouter()
# router.register("payments", PaymentViewSet, basename="payments")

urlpatterns = [
    # path("profile/<int:pk>/", UserProfileView.as_view(), name="user_profile"),
    # path("register/", UserCreateAPIView.as_view(), name="register"),
    # path(
    #     "login/",
    #     MyTokenObtainPairView.as_view(permission_classes=(AllowAny,)),
    #     name="login",
    # ),
    # path(
    #     "token/refresh/",
    #     TokenRefreshView.as_view(permission_classes=(AllowAny,)),
    #     name="token_refresh",
    # ),
    # path("payments/", PaymentAPIView.as_view(), name="payments"),
]

urlpatterns += router.urls
