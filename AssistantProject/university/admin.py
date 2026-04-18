from django.contrib import admin
from .models import Course, CalendarEvent

admin.site.register(Course)
admin.site.register(CalendarEvent)