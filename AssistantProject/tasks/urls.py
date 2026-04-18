from django.urls import path
from .views import daily_tasks_home, settings_view # <--- import it here

urlpatterns = [
    path('', daily_tasks_home, name='tasks_home'),
    path('settings/', settings_view, name='settings'), # <--- add this line
]