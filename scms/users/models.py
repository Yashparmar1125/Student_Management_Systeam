from django.contrib.auth.models import AbstractUser
from django.db import models



class CustomUser(AbstractUser):
    USER=[
        (1,'HOD'),
        (2, 'STAFF'),
        (3, 'STUDENT')
    ]
    user_type=models.CharField(choices=USER,max_length=20,default=1)
    profile_pic=models.ImageField(upload_to='media/profile_pics')
    date_of_birth=models.DateField(null=True)
    mobile_number=models.CharField(max_length=10,null=True)
    Address=models.CharField(max_length=100,null=True)

class Course(models.Model):
    name=models.CharField(max_length=100,null=False)
    intake=models.IntegerField(default=0,null=False)
    short_name=models.CharField(max_length=50,default='',unique=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Session_Year(models.Model):
    session_start=models.CharField(max_length=50)
    session_end=models.CharField(max_length=50)

    def __str__(self):
        return self.session_start + "-" + self.session_end

class Student(models.Model):
    admin=models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    student_id=models.CharField(max_length=50,null=False,unique=True)
    date_of_birth=models.DateField()
    religion=models.CharField(max_length=50,null=False)
    mobile_no=models.CharField(max_length=10,null=False)
    father_name=models.CharField(max_length=50,null=False)
    mother_name=models.CharField(max_length=50,null=False)
    father_no=models.CharField(max_length=10,null=False)
    division=models.CharField(max_length=2,null=False)
    mother_no=models.CharField(max_length=10,null=False)
    permanent_address=models.TextField()
    present_address=models.TextField()
    gender=models.CharField(max_length=50,null=False)
    course_id=models.ForeignKey(Course, on_delete=models.DO_NOTHING,null=False)
    session_id=models.ForeignKey(Session_Year, on_delete=models.DO_NOTHING,null=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.admin.first_name +" "+self.admin.last_name

class Staff(models.Model): #teacher model
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    teacher_id=models.CharField(max_length=50,null=False,unique=True)
    name=models.CharField(max_length=100,null=False)
    gender=models.CharField(max_length=50,null=False)
    date_of_birth=models.DateField()
    phone_number=models.CharField(max_length=10,null=False)
    join_date=models.DateField()
    qualification=models.CharField(max_length=50,null=False)
    experience=models.CharField(max_length=50,null=False)
    address=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.admin.username

class Subjects(models.Model):
    subject_id=models.CharField(max_length=50,null=False,primary_key=True)
    name=models.CharField(max_length=50,null=False)
    course_id=models.ForeignKey(Course, on_delete=models.DO_NOTHING,null=False)
    teacher_id=models.ForeignKey(Staff, on_delete=models.DO_NOTHING,null=False)
    semester=models.CharField(max_length=50,null=False)
    credits=models.CharField(max_length=50,null=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject_id


class Holidays(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50,null=False)
    holiday_type=models.CharField(max_length=50,null=False)
    start_date=models.DateField()
    end_date=models.DateField()
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

from django.db import models

class Room(models.Model):
    ROOM_TYPE_CHOICES = [
        ('class', 'Classroom'),
        ('lab', 'Laboratory'),
    ]

    room_number = models.CharField(max_length=10, unique=True)
    room_type = models.CharField(max_length=5, choices=ROOM_TYPE_CHOICES, null=False)  # Room type field

    def __str__(self):
        return f'{self.room_number} - {self.get_room_type_display()}'

class Timetable(models.Model):
    DAY_CHOICES = [
        ('mon', 'Monday'),
        ('tue', 'Tuesday'),
        ('wed', 'Wednesday'),
        ('thu', 'Thursday'),
        ('fri', 'Friday'),
        ('sat', 'Saturday'),
        ('sun', 'Sunday'),
    ]

    SEMESTER_CHOICES = [
        (1, 'Semester 1'),
        (2, 'Semester 2'),
        (3, 'Semester 3'),
        (4, 'Semester 4'),
        (5, 'Semester 5'),
        (6, 'Semester 6'),
    ]

    LAB_OR_THEORY_CHOICES = [
        ('lab', 'Lab'),
        ('theory', 'Theory'),
    ]

    timetable_id = models.AutoField(primary_key=True)
    subject_name = models.ForeignKey(Subjects, on_delete=models.DO_NOTHING, null=False)
    day = models.CharField(max_length=3, choices=DAY_CHOICES, null=False)
    start_time = models.TimeField()
    end_time = models.TimeField()
    branch = models.ForeignKey(Course, on_delete=models.DO_NOTHING, null=True)
    teacher_id = models.ForeignKey(Staff, on_delete=models.DO_NOTHING, null=False)
    semester = models.IntegerField(choices=SEMESTER_CHOICES, null=False)  # Semester field
    room_no = models.ForeignKey(Room, on_delete=models.DO_NOTHING, null=False)  # Foreign key to Room
    lab_or_theory = models.CharField(max_length=10, choices=LAB_OR_THEORY_CHOICES, null=False)  # Lab/Theory field
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Timetable {self.timetable_id} - {self.get_day_display()} - Semester {self.semester} - {self.room_no} - {self.get_lab_or_theory_display()}'

class Registration(models.Model):
    SEMESTER_CHOICES = [
        (1, 'Semester 1'),
        (2, 'Semester 2'),
        (3, 'Semester 3'),
        (4, 'Semester 4'),
        (5, 'Semester 5'),
        (6, 'Semester 6'),
    ]
    registration_id=models.AutoField(primary_key=True)
    student_id=models.ForeignKey(Student, on_delete=models.DO_NOTHING,null=False)
    semester = models.IntegerField(choices=SEMESTER_CHOICES, null=False)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.student_id} - {self.semester} - {self.registration_id}'

class Assignment(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    subject_id = models.ForeignKey(Subjects, on_delete=models.DO_NOTHING, null=False)
    course_id = models.ForeignKey(Course, on_delete=models.DO_NOTHING, null=False)
    file = models.FileField(upload_to='Assignments/', null=True)
    points = models.IntegerField()
    due_date = models.DateTimeField()
    uploaded_by = models.ForeignKey(Staff, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='submissions/')
    feedback = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('assignment', 'student')

    def __str__(self):
        return f'Submission {self.id} by {self.student.admin.username} for {self.assignment.title}'




class Results(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    isa_marks = models.FloatField(null=True, default=None)  # Internal Assessment marks
    mse_marks = models.FloatField(null=True, default=None)  # Mid-Semester Exam marks
    ese_marks = models.FloatField(null=True, default=None)  # End-Semester Exam marks
    total_marks = models.FloatField(null=True, blank=True, default=None)  # Total marks (calculated)
    uploaded_by=models.ForeignKey(Staff, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'Results for {self.student.admin.username} in {self.subject.name}'

class Note(models.Model):
    NOTE_TYPE_CHOICES = [
        ('subject_note', 'Subject Notes'),
        ('practice_paper', 'Practice Papers'),
    ]

    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='notes/')
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Staff, on_delete=models.CASCADE)
    note_type = models.CharField(max_length=50, choices=NOTE_TYPE_CHOICES)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.note_type})"

class Fess(models.Model):
    fee_id = models.AutoField(primary_key=True)
    transaction_id = models.CharField(max_length=12)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    semester=models.CharField(max_length=10)
    description = models.TextField()
    amount = models.FloatField()
    mode=models.CharField(max_length=100)
    paid_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Fess of {self.student.admin.first_name}"


class Event(models.Model):
    title = models.CharField(max_length=100)
    start = models.DateTimeField()
    end = models.DateTimeField(null=True, blank=True)
    all_day = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Exam_Schedule(models.Model):
    name = models.CharField(max_length=100)
    Branch = models.ForeignKey(Course,on_delete=models.CASCADE)  # or IntegerField if you prefer
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    semester = models.CharField(max_length=10)
    date = models.DateField()
    start_time = models.TimeField()
    exam_type = models.CharField(max_length=50)

    def __str__(self):
        return self.name