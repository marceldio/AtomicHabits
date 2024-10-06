from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.serializers import RegisterSerializer


class RegisterSerializerTest(TestCase):
    def test_valid_data(self):
        data = {
            "email": "testuser@example.com",
            "password": "testpassword",
            "password2": "testpassword",
        }
        serializer = RegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["email"], "testuser@example.com")

    def test_password_mismatch(self):
        data = {
            "email": "testuser@example.com",
            "password": "testpassword",
            "password2": "wrongpassword",
        }
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("password", serializer.errors)

    def test_invalid_registration_data(self):
        data = {"email": "invalid_email", "password": "password", "password2": "pass"}
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("password", serializer.errors)


class UserAPITest(APITestCase):
    def test_login_invalid_credentials(self):
        """Тест на вход с некорректными учетными данными."""
        url = reverse("users:token_obtain_pair")
        response = self.client.post(
            url, {"email": "wrong@example.com", "password": "wrong"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)  # Проверяем, что ошибка связана с email
        self.assertEqual(
            response.data["email"][0], "Пользователь с таким email не найден."
        )
