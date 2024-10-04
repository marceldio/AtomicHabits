from django.urls import path

from habits.apps import HabitsConfig
from habits.views import HabitListView, HabitDetailView

app_name = HabitsConfig.name

urlpatterns = [
    path("", HabitListView.as_view(), name="habit_list"),
    path('<int:pk>/', HabitDetailView.as_view(), name='habit_detail'),
]
