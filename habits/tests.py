from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from habits.tasks import send_habit_reminders
from habits.telegram import send_telegram_message
from users.models import User


class HabitModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com", password="testpassword"
        )

    def test_habit_creation(self):
        """Тест успешного создания привычки."""
        habit = Habit.objects.create(
            user=self.user,
            action="Бег",
            place="Парк",
            time="08:00:00",
            is_pleasant=True,
            period=1,
            duration=60,
        )
        self.assertEqual(habit.user, self.user)
        self.assertEqual(habit.action, "Бег")
        self.assertEqual(habit.place, "Парк")

    def test_habit_validation_error_with_reward_and_linked_habit(self):
        """Тест на валидацию: ошибка при одновременном указании вознаграждения и
        связанной привычки."""
        linked_habit = Habit.objects.create(
            user=self.user,
            action="Приятная привычка",
            place="Дом",
            time="09:00:00",
            is_pleasant=True,
            period=1,
            duration=60,
        )
        habit = Habit(
            user=self.user,
            action="Утренняя зарядка",
            place="Парк",
            time="08:00:00",
            reward="Шоколадка",
            linked_habit=linked_habit,
            period=1,
            duration=60,
        )
        with self.assertRaises(ValidationError):
            """Вызовем валидацию вручную"""
            habit.clean()


class HabitAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com", password="testpassword"
        )
        self.client.force_authenticate(user=self.user)
        """Удаляем все привычки перед тестом"""
        Habit.objects.all().delete()
        self.habit = Habit.objects.create(
            user=self.user,
            action="Бег",
            place="Парк",
            time="08:00:00",
            period=1,
            duration=60,
        )

    def test_get_habit_list(self):
        """Тест на получение списка привычек."""
        url = reverse("habits:habit_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        """Ожидаем одну привычку"""
        self.assertEqual(len(response.data["results"]), 1)

    def test_create_habit(self):
        """Тест на создание привычки через API."""
        url = reverse("habits:habit_list")
        data = {
            "action": "Чтение",
            "place": "Дом",
            "time": "10:00:00",
            "period": 1,
            "duration": 60,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 2)

    def test_update_habit(self):
        """Тест на обновление привычки."""
        url = reverse("habits:habit_detail", args=[self.habit.id])
        data = {
            "action": "Обновленный бег",
            "place": "Офис",
            "time": "07:30:00",
            "period": 2,
            "duration": 60,
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.habit.refresh_from_db()
        self.assertEqual(self.habit.action, "Обновленный бег")

    def test_delete_habit(self):
        """Тест на удаление привычки."""
        url = reverse("habits:habit_detail", args=[self.habit.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.count(), 0)


class HabitModelValidationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com", password="testpassword"
        )

    def test_habit_with_linked_habit_and_reward_raises_error(self):
        """Тест: ошибка при одновременном указании вознаграждения и
        связанной привычки."""
        linked_habit = Habit.objects.create(
            user=self.user,
            action="Приятная привычка",
            place="Дом",
            time="09:00:00",
            is_pleasant=True,
            period=1,
            duration=60,
        )
        habit = Habit(
            user=self.user,
            action="Утренняя зарядка",
            place="Парк",
            time="08:00:00",
            reward="Шоколадка",
            linked_habit=linked_habit,
            period=1,
            duration=60,
        )
        with self.assertRaises(ValidationError):
            """Проверка валидации вручную"""
            habit.clean()

    def test_habit_with_duration_exceeds_limit_raises_error(self):
        """Тест: ошибка при превышении времени на выполнение более 120 секунд."""
        habit = Habit(
            user=self.user,
            action="Долгое упражнение",
            place="Зал",
            time="10:00:00",
            duration=130,  # Время больше допустимого
            period=1,
        )
        with self.assertRaises(ValidationError):
            habit.clean()

    def test_habit_with_unpleasant_linked_habit_raises_error(self):
        """Тест: ошибка при привязке неприятной привычки в качестве связанной."""
        unpleasant_habit = Habit.objects.create(
            user=self.user,
            action="Неприятная привычка",
            place="Офис",
            time="11:00:00",
            is_pleasant=False,
            period=1,
            duration=60,
        )
        habit = Habit(
            user=self.user,
            action="Приятная привычка",
            place="Дом",
            time="09:00:00",
            linked_habit=unpleasant_habit,
            period=1,
            duration=60,
        )
        with self.assertRaises(ValidationError):
            habit.clean()

    def test_pleasant_habit_with_reward_raises_error(self):
        """Тест: ошибка при указании вознаграждения для приятной привычки."""
        habit = Habit(
            user=self.user,
            action="Приятная зарядка",
            place="Парк",
            time="08:00:00",
            is_pleasant=True,
            reward="Шоколадка",
            period=1,
            duration=60,
        )
        with self.assertRaises(ValidationError):
            habit.clean()

    def test_habit_with_period_exceeds_limit_raises_error(self):
        """Тест: ошибка при указании периодичности более 7 дней."""
        habit = Habit(
            user=self.user,
            action="Редкая привычка",
            place="Дом",
            time="09:00:00",
            period=8,  # Период больше допустимого
            duration=60,
        )
        with self.assertRaises(ValidationError):
            habit.clean()

    def test_valid_habit(self):
        """Тест: успешное создание валидной привычки."""
        habit = Habit(
            user=self.user,
            action="Бег",
            place="Парк",
            time="08:00:00",
            period=1,
            duration=60,
        )
        try:
            """Проверяем, что нет ошибок валидации"""
            habit.clean()
        except ValidationError:
            self.fail("Habit raised ValidationError unexpectedly!")


class HabitTasksTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com", password="testpassword"
        )

        """Создаем привычку, которая выполняется через 15 минут от текущего времени"""
        current_time = timezone.now()
        self.habit = Habit.objects.create(
            user=self.user,
            action="Бег",
            place="Парк",
            time=(current_time + timezone.timedelta(minutes=15)).time(),
            period=1,
            duration=60,
        )

    @patch("habits.tasks.send_telegram_message")
    def test_send_habit_reminders(self, mock_send_telegram_message):
        """Ожидаем, что не будет вызова send_telegram_message, если нет chat_id"""
        send_habit_reminders()
        mock_send_telegram_message.assert_not_called()

    @patch("habits.tasks.send_telegram_message")
    def test_no_habits_for_reminders(self, mock_send_telegram_message):
        """Удаляем все привычки"""
        Habit.objects.all().delete()
        send_habit_reminders()
        """Проверяем, что функция отправки сообщения НЕ была вызвана"""
        mock_send_telegram_message.assert_not_called()

    @patch("habits.tasks.send_telegram_message")
    def test_send_habit_reminders_no_chat_id(self, mock_send_telegram_message):
        self.user.chat_id = None
        self.user.save()
        send_habit_reminders()

        """Проверяем, что функция отправки сообщения НЕ была вызвана"""
        mock_send_telegram_message.assert_not_called()


class TelegramTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com", password="testpassword", chat_id="123456"
        )

    @patch("habits.telegram.requests.post")
    def test_send_telegram_message(self, mock_post):
        send_telegram_message(self.user, "Test message")
        """Проверяем, что запрос был отправлен"""
        mock_post.assert_called_once()
