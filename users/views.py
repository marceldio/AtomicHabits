from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from users.models import User
from users.serializers import RegisterSerializer

# Представление для регистрации пользователя
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

# Представление для выхода (logout), которое деактивирует refresh токен
class LogoutView(generics.GenericAPIView):
    permission_classes = (AllowAny,)  # Позволяем любому пользователю выходить (если у него есть refresh токен)

    def post(self, request):
        try:
            # Получаем refresh токен из запроса
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            # Деактивируем токен
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
