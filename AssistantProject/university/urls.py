from django.urls import path
from .views import university_home

urlpatterns = [
    path('', university_home, name='university_home'),
]