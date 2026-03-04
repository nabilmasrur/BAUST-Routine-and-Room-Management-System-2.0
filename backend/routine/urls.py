from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DepartmentViewSet,
    TeacherViewSet,
    CourseViewSet,
    RoomViewSet,
    RoutineInfoViewSet,
    ScheduleViewSet
)

router = DefaultRouter()
router.register(r'departments', DepartmentViewSet)
router.register(r'teachers', TeacherViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'rooms', RoomViewSet)
router.register(r'routines', RoutineInfoViewSet)
router.register(r'schedules', ScheduleViewSet)

urlpatterns = [
    path('', include(router.urls)),
]