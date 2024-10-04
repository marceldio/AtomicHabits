from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated

from habits.models import Habit
from habits.serializers import HabitSerializer


# Представление для списка привычек и создания новой привычки
class HabitListView(generics.ListCreateAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Фильтруем привычки только текущего пользователя
        return Habit.objects.filter(user=self.request.user).order_by("id")

    def perform_create(self, serializer):
        # Привязываем новую привычку к текущему пользователю
        serializer.save(user=self.request.user)


# Представление для получения, обновления или удаления одной привычки
class HabitDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Фильтруем привычки только текущего пользователя
        return Habit.objects.filter(user=self.request.user)
