from django.contrib import admin
from django.urls import path, include
from routine.views import login_view, save_full_routine, get_available_rooms # শুধু login_view এবং save_full_routine থাকবে

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', login_view, name='api_login'),
    path('api/save_routine/', save_full_routine, name='save_full_routine'),
    path('api/available_rooms/', get_available_rooms, name='available_rooms'),
    path('api/', include('routine.urls')),
]