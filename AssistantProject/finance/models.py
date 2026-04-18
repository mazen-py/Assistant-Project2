from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    CATEGORY_CHOICES = [
        ('Food', 'Food & Dining'),
        ('Transport', 'Transportation'),
        ('Shopping', 'Shopping'),
        ('Bills', 'Bills & Utilities'),
        ('Entertainment', 'Entertainment'),
        ('Other', 'Other'),
    ]
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    is_income = models.BooleanField(default=False)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Other')

    def __str__(self):
        return self.description