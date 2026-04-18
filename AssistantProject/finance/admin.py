from django.contrib import admin
from .models import Account, Transaction

# Register your models here so they appear in the /admin/ dashboard
admin.site.register(Account)
admin.site.register(Transaction)