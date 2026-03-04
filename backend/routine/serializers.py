from rest_framework import serializers
from .models import Department, Teacher, Course, Room, RoutineInfo, Schedule

class DepartmentSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")
    class Meta:
        model = Department
        fields = '__all__'

class TeacherSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    course_codes = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Teacher
        # ✅ 'created_at' কে fields list এ যোগ করুন
        fields = ['id', 'short_name', 'full_name', 'department', 'department_name', 'email', 'phone', 'is_active', 'courses', 'course_codes', 'created_at']

    def get_course_codes(self, obj):
        return [course.course_code for course in obj.courses.all()]

# TeacherSerializer এর উপরে বা নিচে এই ছোট Serializer টা যোগ করুন
class SimpleTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'short_name', 'full_name']

class CourseSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    created_at = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")
    # ✅ NEW: Show assigned teachers with the course
    teachers = SimpleTeacherSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = '__all__'
        
class RoomSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")
    class Meta:
        model = Room
        fields = '__all__'

# ... (Department, Course, Teacher, Room Serializers) ...

# ✅ FIX: RoutineInfoSerializer is defined BEFORE ScheduleSerializer
class RoutineInfoSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    created_at = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")
    
    class Meta:
        model = RoutineInfo
        fields = '__all__'

# ✅ FIX: ScheduleSerializer is defined AFTER RoutineInfoSerializer
class ScheduleSerializer(serializers.ModelSerializer):
    course_details = CourseSerializer(source='course', read_only=True)
    teacher_details = TeacherSerializer(source='teacher', read_only=True)
    room_details = RoomSerializer(source='room', read_only=True)
    
    # Now Python will know what 'RoutineInfoSerializer' is
    routine_details = RoutineInfoSerializer(source='routine', read_only=True) 
    
    created_at = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")
    
    class Meta:
        model = Schedule
        fields = '__all__'