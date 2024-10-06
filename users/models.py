from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

NULLABLE = {"blank": True, "null": True}


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Email")

    phone = models.CharField(max_length=35, verbose_name="Телефон", **NULLABLE)
    tg_name = models.CharField(max_length=50, verbose_name="Ник в Telegram", **NULLABLE)
    chat_id = models.CharField(
        max_length=50, verbose_name="Telegram Chat ID", **NULLABLE
    )
    country = models.CharField(max_length=100, verbose_name="Страна", **NULLABLE)
    avatar = models.ImageField(
        upload_to="users/avatars/", verbose_name="Аватар", **NULLABLE
    )
    token = models.CharField(max_length=255, verbose_name="Токен", **NULLABLE)

    USERNAME_FIELD = "email"
    """Нет дополнительных обязательных полей"""
    REQUIRED_FIELDS = []

    """Указываем кастомный менеджер"""
    objects = CustomUserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
