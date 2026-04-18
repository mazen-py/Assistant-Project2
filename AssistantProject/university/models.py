from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=100)
    credits = models.IntegerField()
    grade_points = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)

    def __str__(self):
        return self.name

class CalendarEvent(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateTimeField()
    event_type = models.CharField(max_length=50)

    def __str__(self):
        return self.title