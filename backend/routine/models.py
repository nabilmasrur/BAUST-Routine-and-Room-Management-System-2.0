from django.db import models

# ==========================================================
#  MODELS - Correct Order
# ==========================================================

class Department(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'departments'
    
    def __str__(self):
        return self.name

# ✅ FIX: Course model is defined BEFORE Teacher model
class Course(models.Model):
    course_code = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=200)
    credit = models.DecimalField(max_digits=3, decimal_places=1)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    is_lab = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'courses'
    
    def __str__(self):
        return f"{self.course_code} - {self.title}"

# ✅ FIX: Teacher model is defined AFTER Course model
class Teacher(models.Model):
    short_name = models.CharField(max_length=10, unique=True)
    full_name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    email = models.EmailField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    
    # Now, this ManyToManyField will work because Python already knows what 'Course' is.
    courses = models.ManyToManyField(Course, blank=True, related_name='teachers')
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'teachers'
    
    def __str__(self):
        return f"{self.short_name} - {self.full_name}"

class Room(models.Model):
    ROOM_TYPE_CHOICES = [
        ('classroom', 'Classroom'),
        ('lab', 'Lab'),
    ]
    room_number = models.CharField(max_length=20, unique=True)
    capacity = models.IntegerField()
    room_type = models.CharField(max_length=10, choices=ROOM_TYPE_CHOICES)
    has_projector = models.BooleanField(default=False)
    has_ac = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'rooms'
    
    def __str__(self):
        return self.room_number

class RoutineInfo(models.Model):
    SEMESTER_CHOICES = [('Summer', 'Summer'), ('Winter', 'Winter')]
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    semester = models.CharField(max_length=10, choices=SEMESTER_CHOICES)
    year = models.IntegerField()
    level_term = models.CharField(max_length=10)
    section = models.CharField(max_length=5)
    advisor_name = models.CharField(max_length=100)
    advisor_phone = models.CharField(max_length=15)
    dpc_name = models.CharField(max_length=100, null=True, blank=True)
    dpc_phone = models.CharField(max_length=15, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'routines'
    
    def __str__(self):
        return f"{self.level_term} - Section {self.section}"

class Schedule(models.Model):
    DAY_CHOICES = [('Sunday', 'Sunday'), ('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday')]
    routine = models.ForeignKey(RoutineInfo, on_delete=models.CASCADE, related_name='schedules')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=10, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    duration_hours = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'schedules'
    
    def __str__(self):
        return f"{self.course.course_code} - {self.day_of_week} {self.start_time}"