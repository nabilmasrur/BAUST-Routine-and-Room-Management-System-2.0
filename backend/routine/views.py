from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from django.db.models import Q
from datetime import datetime, timedelta, time

# Assuming models and serializers are correctly imported
from .models import Department, Teacher, Course, Room, RoutineInfo, Schedule
from .serializers import (
    DepartmentSerializer, 
    TeacherSerializer, 
    CourseSerializer, 
    RoomSerializer, 
    RoutineInfoSerializer,
    ScheduleSerializer
)

# ===============================================
#  Viewset Classes (UNCHANGED)
# ===============================================
class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all().order_by('name')
    serializer_class = DepartmentSerializer
class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all().order_by('full_name')
    serializer_class = TeacherSerializer
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all().order_by('course_code')
    serializer_class = CourseSerializer
class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all().order_by('room_number')
    serializer_class = RoomSerializer
class RoutineInfoViewSet(viewsets.ModelViewSet):
    queryset = RoutineInfo.objects.all()
    serializer_class = RoutineInfoSerializer
class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all().select_related('routine', 'course', 'teacher', 'room')
    serializer_class = ScheduleSerializer
    def get_queryset(self):
        queryset = super().get_queryset()
        day = self.request.query_params.get('day', None)
        if day:
            queryset = queryset.filter(day_of_week__iexact=day)
        return queryset


# ===============================================
#  Custom API Functions
# ===============================================

@api_view(['POST'])
def login_view(request):
    """
    API endpoint for user login.
    """
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(request, username=username, password=password)
    
    if user is not None:
        login(request, user)
        return Response({
            'success': True, 
            'message': 'Login successful', 
            'username': user.username
        }, status=status.HTTP_200_OK)
    else:
        return Response({
            'success': False, 
            'message': 'Invalid username or password'
        }, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def save_full_routine(request):
    """
    Saves RoutineInfo and all associated Schedules after pre-validation.
    FIX: Uses string format for time comparison in the database query (most robust method).
    """
    try:
        data = request.data
        schedules_data = data.get('schedules', [])
        
        # --- Pre-Validation: Check for conflicts across all new schedules ---
        for item in schedules_data:
            day = item.get('day_of_week')
            start_time_str = item.get('start_time') # e.g., "08:00:00"
            duration = item.get('duration_hours', 1)
            teacher_id = item.get('teacher')
            room_id = item.get('room')
            
            # Calculate start/end time objects
            start_time_dt_obj = datetime.strptime(start_time_str, '%H:%M:%S').time()
            end_time_dt_obj = (datetime.combine(datetime.today(), start_time_dt_obj) + timedelta(hours=duration)).time()
            
            # 💡 CRITICAL FIX: Convert times to HH:MM:SS strings for reliable MySQL comparison
            new_start_time_str = start_time_str
            new_end_time_str = end_time_dt_obj.strftime('%H:%M:%S')

            # The robust overlap query using string times
            # Existing Start < New End AND Existing End > New Start
            overlap_query = Q(start_time__lt=new_end_time_str) & Q(end_time__gt=new_start_time_str)

            # 1. Check ROOM CONFLICT
            room_conflict = Schedule.objects.filter(
                Q(room_id=room_id) & Q(day_of_week=day) & overlap_query
            ).exists()
            if room_conflict:
                room_num = Room.objects.get(id=room_id).room_number
                return Response({'error': f'Room Conflict: Room {room_num} is already booked on {day} at {start_time_str}.'}, status=status.HTTP_409_CONFLICT)

            # 2. Check TEACHER CONFLICT
            teacher_conflict = Schedule.objects.filter(
                Q(teacher_id=teacher_id) & Q(day_of_week=day) & overlap_query
            ).exists()
            if teacher_conflict:
                teacher_sn = Teacher.objects.get(id=teacher_id).short_name
                return Response({'error': f'Teacher Conflict: {teacher_sn} is already teaching on {day} at {start_time_str}.'}, status=status.HTTP_409_CONFLICT)

        # --- Step 1: Create RoutineInfo ---
        routine_info = RoutineInfo.objects.create(
            department_id=data.get('department'),
            semester=data.get('semester'),
            year=data.get('year'),
            level_term=data.get('level_term'),
            section=data.get('section'),
            advisor_name=data.get('advisor_name'),
            advisor_phone=data.get('advisor_phone'),
            dpc_name=data.get('dpc_name'),
            dpc_phone=data.get('dpc_phone')
        )
        
        # --- Step 2: Create Schedules ---
        schedule_objects = []
        for item in schedules_data:
            # For saving to TimeField, we use the time objects
            start_time_dt = datetime.strptime(item.get('start_time'), '%H:%M:%S').time()
            end_time_dt = (datetime.combine(datetime.today(), start_time_dt) + timedelta(hours=item.get('duration_hours', 1))).time()
            
            schedule_objects.append(
                Schedule(
                    routine=routine_info,
                    course_id=item.get('course'),
                    teacher_id=item.get('teacher'),
                    room_id=item.get('room'),
                    day_of_week=item.get('day_of_week'),
                    start_time=start_time_dt, 
                    end_time=end_time_dt, 
                    duration_hours=item.get('duration_hours', 1)
                )
            )
        
        Schedule.objects.bulk_create(schedule_objects)
        
        return Response({'message': 'Routine saved successfully!'}, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({'error': f'Server Error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_available_rooms(request):
    """
    Returns available rooms for a given day, start_time, duration, and checks if the specific teacher is free.
    FIX: Uses string format for time comparison.
    """
    try:
        day = request.query_params.get('day')
        start_time_str = request.query_params.get('start_time') # HH:MM:SS
        duration_str = request.query_params.get('duration', '1') 
        teacher_id = request.query_params.get('teacher_id') 
        
        if not day or not start_time_str:
            return Response({'error': 'Day and start_time are required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Calculate end time (as time object)
        start_time_obj = datetime.strptime(start_time_str, '%H:%M:%S').time()
        duration_hours = int(duration_str)
        end_time_obj = (datetime.combine(datetime.today(), start_time_obj) + timedelta(hours=duration_hours)).time()
        
        # 💡 CRITICAL FIX: Convert times to HH:MM:SS strings for reliable MySQL comparison
        new_start_time_str = start_time_str
        new_end_time_str = end_time_obj.strftime('%H:%M:%S')

        # Robust Overlap Query using string times
        overlap_query = Q(start_time__lt=new_end_time_str) & Q(end_time__gt=new_start_time_str)
        
        # --- 1. Check TEACHER CONFLICT ---
        teacher_is_booked = False
        if teacher_id and teacher_id != 'null':
            teacher_conflict = Schedule.objects.filter(
                Q(teacher_id=teacher_id) & Q(day_of_week=day) & overlap_query
            ).exists()
            if teacher_conflict:
                teacher_is_booked = True
        
        # --- 2. Find OCCUPIED ROOMS (Room CONFLICT) ---
        occupied_rooms_ids = Schedule.objects.filter(
            Q(day_of_week=day) & overlap_query
        ).values_list('room_id', flat=True).distinct()

        # --- 3. Get Available Rooms ---
        available_rooms = Room.objects.exclude(id__in=occupied_rooms_ids)
        
        # --- 4. Serialize Data ---
        serializer = RoomSerializer(available_rooms, many=True)
        
        response_data = {
            'rooms': serializer.data,
            'teacher_booked': teacher_is_booked
        }
        
        return Response(response_data)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)