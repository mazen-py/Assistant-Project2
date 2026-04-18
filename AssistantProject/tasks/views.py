from datetime import date
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .models import Task

# ==========================================
# AUTHENTICATION VIEWS
# ==========================================
def custom_login(request):
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
    else:
        form = AuthenticationForm()
    return render(request, 'tasks/login.html', {'form': form})

def custom_register(request):
    if request.user.is_authenticated:
        return redirect('/')
        
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'tasks/register.html', {'form': form})

def custom_logout(request):
    logout(request)
    return redirect('login')

# ==========================================
# APP VIEWS
# ==========================================
@login_required(login_url='/login/')
def daily_tasks_home(request):
    today = date.today()
    # FIX: Changed 'completed=False' to 'is_completed=False' to match your model
    # FIX: Changed 'due_date' to 'deadline' based on the traceback choices
    all_tasks = Task.objects.filter(user=request.user, is_completed=False)

    context = {
        'overdue': all_tasks.filter(deadline__lt=today),
        'today': all_tasks.filter(deadline=today),
        'upcoming': all_tasks.filter(deadline__gt=today),
    }
    return render(request, 'tasks/home.html', context)

@login_required(login_url='/login/')
def settings_view(request):
    password_form = PasswordChangeForm(request.user)
    msg = None
    
    if request.method == 'POST':
        if 'update_username' in request.POST:
            new_username = request.POST.get('new_username')
            if new_username:
                request.user.username = new_username
                request.user.save()
                msg = "Username updated successfully!"
                
        elif 'update_password' in request.POST:
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                msg = "Password updated successfully!"
                
    return render(request, 'tasks/settings.html', {'password_form': password_form, 'msg': msg})