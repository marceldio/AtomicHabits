from rest_framework import generics, serializers, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from users.serializers import RegisterSerializer, UserProfileSerializer


# Представление для регистрации пользователя
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


# Представление для выхода (logout), которое деактивирует refresh токен
class LogoutView(generics.GenericAPIView):
    permission_classes = [
        AllowAny
    ]  # Позволяем любому пользователю выходить (если у него есть refresh токен)
    serializer_class = None

    # Добавим фейковый сериализатор для Swagger
    class FakeSerializer(serializers.Serializer):
        pass

    def get_serializer_class(self):
        # Проверка для Swagger-документации
        if getattr(self, "swagger_fake_view", False):
            return self.FakeSerializer
        return None

    def post(self, request):
        try:
            # Проверяем наличие refresh токена в запросе
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response(
                    {"detail": "Refresh token is missing."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Деактивируем токен
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# Представление для редактирования профиля пользователя
class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_object(self):
        # Возвращаем текущего аутентифицированного пользователя
        return self.request.user
