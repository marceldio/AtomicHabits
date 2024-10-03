from django.db import models
from django.core.exceptions import ValidationError
from users.models import User


class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='habits')
    place = models.CharField(max_length=255)
    time = models.TimeField()
    action = models.CharField(max_length=255)
    is_pleasant = models.BooleanField(default=False)
    linked_habit = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    period = models.PositiveIntegerField(default=1)  # По умолчанию ежедневно
    reward = models.CharField(max_length=255, null=True, blank=True)
    duration = models.PositiveIntegerField()  # Время выполнения в секундах
    is_public = models.BooleanField(default=False)

    def clean(self):
        # Валидатор на одновременный выбор связанной привычки и вознаграждения
        if self.reward and self.linked_habit:
            raise ValidationError('Нельзя указать одновременно вознаграждение и связанную привычку.')

        # Валидатор на время выполнения (не более 120 секунд)
        if self.duration > 120:
            raise ValidationError('Время выполнения не может превышать 120 секунд.')

        # Связанные привычки могут быть только с признаком приятных
        if self.linked_habit and not self.linked_habit.is_pleasant:
            raise ValidationError('Связанная привычка должна быть приятной.')

        # Приятная привычка не может иметь вознаграждения или связанных привычек
        if self.is_pleasant and (self.reward or self.linked_habit):
            raise ValidationError('Приятная привычка не может иметь вознаграждения или связанных привычек.')

        # Периодичность должна быть не реже одного раза в неделю
        if self.period > 7:
            raise ValidationError('Нельзя выполнять привычку реже одного раза в неделю.')

    def __str__(self):
        return f'{self.action} в {self.time}'

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
        ordering = ['-time']
