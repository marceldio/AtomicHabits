from celery import shared_task
from django.utils import timezone

from habits.models import Habit

from .telegram import send_telegram_message

"""Задача для отправки напоминаний о привычках в текущее время (UTC)"""


@shared_task
def send_habit_reminders():
    """Получаем текущее время"""
    current_time = timezone.now()
    """Вычисляем время через 30 минут"""
    time_in_30_minutes = current_time + timezone.timedelta(minutes=30)

    """Фильтруем привычки, которые нужно выполнить в ближайшие 30 минут"""
    habits = Habit.objects.filter(
        time__gte=current_time.time(), time__lte=time_in_30_minutes.time()
    ).order_by("time")

    for habit in habits:
        user = habit.user
        """Проверяем наличие chat_id у пользователя"""
        if user.chat_id:
            message = f"Напоминание: {habit.action} в {habit.place} в {habit.time}"
            send_telegram_message(user, message)
            print(
                f"Сообщение отправлено пользователю {user.email} "
                f"о задаче {habit.action}"
            )
        else:
            print(
                f"У пользователя {user.email} отсутствует chat_id, "
                f"сообщение не отправлено."
            )
