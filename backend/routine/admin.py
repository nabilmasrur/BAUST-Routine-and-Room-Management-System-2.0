from django.contrib import admin
from .models import Department, Teacher, Course, Room, RoutineInfo, Schedule

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']
    search_fields = ['name', 'code']

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['short_name', 'full_name', 'department', 'email', 'is_active']
    search_fields = ['short_name', 'full_name', 'email']
    list_filter = ['department', 'is_active']

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['course_code', 'title', 'credit', 'department', 'is_lab']
    search_fields = ['course_code', 'title']
    list_filter = ['department', 'is_lab']

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_number', 'capacity', 'room_type', 'has_projector', 'has_ac', 'is_available']
    search_fields = ['room_number']
    list_filter = ['room_type', 'is_available']

@admin.register(RoutineInfo)
class RoutineInfoAdmin(admin.ModelAdmin):
    list_display = ['level_term', 'section', 'semester', 'year', 'advisor_name']
    list_filter = ['semester', 'year', 'level_term', 'section']

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['course', 'teacher', 'room', 'day_of_week', 'start_time', 'end_time']
    search_fields = ['course__course_code', 'teacher__full_name']
    list_filter = ['day_of_week', 'routine']