from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    # 1. Security: Links the task to the logged-in user
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    # 2. Task Details
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    
    # 3. Time & Status Management
    deadline = models.DateField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    
    # 4. Extra Settings
    task_type = models.CharField(max_length=50, null=True, blank=True)
    warning_triggered = models.BooleanField(default=False)

    def __str__(self):
        return self.title