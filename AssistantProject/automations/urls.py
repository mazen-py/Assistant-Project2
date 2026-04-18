from django.urls import path
from . import views

urlpatterns = [
    path('', views.automations_home, name='automations_home'),
]