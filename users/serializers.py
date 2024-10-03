from rest_framework import serializers
from users.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password2', 'phone', 'tg_name', 'country', 'avatar')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Пароли не совпадают."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            phone=validated_data.get('phone', ''),
            tg_name=validated_data.get('tg_name', ''),
            country=validated_data.get('country', ''),
            avatar=validated_data.get('avatar', None),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Добавляем email в токен
        token['email'] = user.email
        return token

    def validate(self, attrs):
        # Заменяем username на email для аутентификации
        email = attrs.get("email", "")
        password = attrs.get("password", "")

        user = User.objects.filter(email=email).first()
        if user and user.check_password(password):
            return super().validate({
                'username': user.email,  # Используем email для генерации токена
                'password': password
            })
        raise serializers.ValidationError({"detail": "Неправильный email или пароль."})
