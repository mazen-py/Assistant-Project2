from django import forms
from .models import Transaction, Account

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'balance']

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        # Notice we added 'category' here!
        fields = ['account', 'description', 'amount', 'category', 'is_income']