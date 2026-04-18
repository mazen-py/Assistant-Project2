from django.contrib import admin
from django.urls import path, include
from tasks.views import custom_login, custom_register, custom_logout

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Your Custom Authentication Gates
    path('login/', custom_login, name='login'),
    path('register/', custom_register, name='register'),
    path('logout/', custom_logout, name='logout'),
    
    # Your Apps
    path('', include('tasks.urls')),
    path('finance/', include('finance.urls')),
    path('university/', include('university.urls')),
    path('automations/', include('automations.urls')),
]