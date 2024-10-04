from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from habits.models import Habit

from .telegram import send_telegram_message


# Задача для отправки напоминаний о привычках в текущее время (UTC)
@shared_task
def send_habit_reminders():
    # Получаем текущее время
    current_time = timezone.now()
    print(f"Задача send_habit_reminders запущена в {current_time} (UTC)")

    # Вычисляем время через 30 минут
    time_in_30_minutes = current_time + timedelta(minutes=30)

    # Фильтруем привычки, которые нужно выполнить в ближайшие 30 минут
    habits = Habit.objects.filter(
        time__gte=current_time.time(), time__lte=time_in_30_minutes.time()
    ).order_by("time")

    if not habits.exists():
        print("Нет привычек для напоминаний на ближайшие 30 минут")

    for habit in habits:
        user = habit.user
        message = f"Напоминание: {habit.action} в {habit.place} в {habit.time}"
        send_telegram_message(user, message)
        print(f"Сообщение отправлено пользователю {user.email} о задаче {habit.action}")
