from rest_framework import serializers
from habits.models import Habit

class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = ['id', 'user', 'action', 'place', 'time', 'is_pleasant', 'linked_habit', 'period', 'reward', 'duration', 'is_public']
        read_only_fields = ['user']  # Поле user должно быть только для чтения
