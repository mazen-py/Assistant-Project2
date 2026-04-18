from django.shortcuts import render
from .models import Course, CalendarEvent
from django.db.models import Sum
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def university_home(request):
    return render(request, 'university/home.html')

def university_home(request):
    courses = Course.objects.all()
    # Grabs the next 5 upcoming calendar events, sorted by date
    events = CalendarEvent.objects.all().order_by('date')[:5] 
    
    # --- CGPA Calculation Logic ---
    # 1. Get the total number of credit hours
    total_credits = courses.aggregate(Sum('credits'))['credits__sum'] or 0
    
    if total_credits > 0:
        # 2. Multiply each course's credits by its grade points, then divide by total credits
        quality_points = sum(course.credits * float(course.grade_points) for course in courses)
        cgpa = round(quality_points / total_credits, 2)
    else:
        # Defaults to 0.00 before your first grades are entered
        cgpa = 0.00 
        
    context = {
        'courses': courses,
        'events': events,
        'cgpa': cgpa,
        'total_credits': total_credits
    }
    return render(request, 'university/home.html', context)