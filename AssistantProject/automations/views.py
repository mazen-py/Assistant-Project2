from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def automations_home(request):
    return render(request, 'automations/home.html')