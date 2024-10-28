from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from users.models import Student,CustomUser,Course,Session_Year,Staff,Subjects,Holidays,Timetable,Room,Fess,Event,Exam_Schedule
from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse
from datetime import datetime, timedelta
import random
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q





@login_required
def HOME(request):
    student_number=Student.objects.count()
    departments_number=Course.objects.count()
    teacher_number=Staff.objects.count()
    context={'student_number':student_number,'departments_number':departments_number,'teacher_number':teacher_number}
    return render(request, 'users/Hod/home.html',context)


@login_required
def student_list(request):
    students = Student.objects.all()
    context = {'students': students}
    return render(request, 'users/Hod/student_list.html', context)


@login_required
def student_add(request):
    course = Course.objects.all()
    sessions = Session_Year.objects.all()
    context = {'course': course, 'sessions': sessions}

    if request.method == 'POST':
        first_name = request.POST.get('first_name').strip()
        last_name = request.POST.get('last_name').strip()
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        religion = request.POST.get('religion')
        course_id = request.POST.get('course_id')
        division = request.POST.get('division')
        session_id = request.POST.get('session_id')
        mobile_no = request.POST.get('mobile_no')
        email = request.POST.get('email')
        father_name = request.POST.get('father_name')
        mother_name = request.POST.get('mother_name')
        father_no = request.POST.get('father_no')
        mother_no = request.POST.get('mother_no')
        present_address = request.POST.get('present_address')
        permanent_address = request.POST.get('permanent_address')
        student_image = request.FILES.get('student_image')

        base_username = f"{first_name.lower()}.{last_name.lower()}"
        username = base_username
        count = 1

        # Ensure the username is unique
        while CustomUser.objects.filter(username=username).exists():
            username = f"{base_username}{count}"
            count += 1

        year = datetime.now().year % 100  # Last two digits of the current year
        course = Course.objects.get(name=course_id)  # Fetch the course object
        branch_code = course.short_name[:2].upper()  # Assuming short_name is something like "Computer Science"

        # Generate a unique student number (e.g., 0037)
        student_count = Student.objects.filter(course_id=course, division=division).count() + 1
        student_number = f"{student_count:04d}"  # Pad with zeros to ensure it's 4 digits

        # Generate the initial student ID
        student_id = f"{year}{branch_code}{division}{student_number}"

        # Ensure student_id is unique
        while Student.objects.filter(student_id=student_id).exists():
            student_count += 1  # Increment the count to get a new student number
            student_number = f"{student_count:04d}"
            student_id = f"{year}{branch_code}{division}{student_number}"

        # Generate password
        password = f"{first_name.lower()}@123"
        print(password, student_id, username)

        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request, 'Username already taken!!!')
            return redirect('student_add')
        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request, 'Email already taken!!!')
            return redirect('student_add')
        else:
            user = CustomUser(first_name=first_name, last_name=last_name, username=username, email=email,
                              profile_pic=student_image, user_type=3)
            user.set_password(password)
            user.save()

            course = Course.objects.get(name=course_id)
            session = Session_Year.objects.get(id=session_id)

            student = Student(admin=user,
                              student_id=student_id,
                              gender=gender,
                              date_of_birth=dob,
                              religion=religion,
                              mobile_no=mobile_no,
                              father_name=father_name,
                              mother_name=mother_name,
                              father_no=father_no,
                              mother_no=mother_no,
                              division=division,
                              present_address=present_address,
                              permanent_address=permanent_address,
                              session_id=session,
                              course_id=course
                              )
            student.save()

            # Send email with credentials
            subject = 'Your Account Credentials'
            message = f"""
                        Hi {first_name},
                        Welcome to Vidyalankar SCMS..
                        Your account has been successfully created.

                        Username: {username}
                        Password: {password}

                        Please log in to your account.

                        Best regards,
                        Team NEXGEN19
                        """
            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
            except Exception as e:
                # Log the error if needed, or handle it quietly
                print(f"Error sending email: {e}")

            messages.success(request, 'Student Added Successfully')
            return redirect('student_list')

    return render(request, 'users/Hod/student_add.html', context)



@login_required
def STUDENT_EDIT(request,student_id):
    student = Student.objects.filter(id=student_id)
    course = Course.objects.all()
    sessions = Session_Year.objects.all()
    context = {'student':student,'course':course,'sessions':sessions}
    return render(request, 'users/Hod/student_edit.html',context)

@login_required
def STUDENT_UPDATE(request):
    course = Course.objects.all()
    sessions = Session_Year.objects.all()

    if request.method == 'POST':
        student_id = request.POST.get('id')

        # User fields
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        student_image = request.FILES.get('student_image')

        # Student fields
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        religion = request.POST.get('religion')
        division = request.POST.get('division')
        course_id = request.POST.get('course_id')
        session_id = request.POST.get('session_id')
        mobile_no = request.POST.get('mobile_no')
        father_name = request.POST.get('father_name')
        mother_name = request.POST.get('mother_name')
        father_no = request.POST.get('father_no')
        mother_no = request.POST.get('mother_no')
        present_address = request.POST.get('present_address')
        permanent_address = request.POST.get('permanent_address')

        # Get current user and student instances
        user = CustomUser.objects.get(id=student_id)
        student = Student.objects.get(admin=student_id)

        # Update user fields if present
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if username:
            user.username = username
        if email:
            user.email = email
        if password:
            user.set_password(password)  # Hash the password
            print("New hashed password:", user.password)  # Debug: Check hashed password
        if student_image:
            user.profile_pic = student_image

        user.save()  # Save user updates

        # Update student fields if present
        if gender:
            student.gender = gender
        if dob:
            student.date_of_birth = dob
        if religion:
            student.religion = religion
        if mobile_no:
            student.mobile_no = mobile_no
        if father_name:
            student.father_name = father_name
        if mother_name:
            student.mother_name = mother_name
        if father_no:
            student.father_no = father_no
        if mother_no:
            student.mother_no = mother_no
        if division:
            student.division = division
        if present_address:
            student.present_address = present_address
        if permanent_address:
            student.permanent_address = permanent_address
        if session_id:
            student.session_id = Session_Year.objects.get(id=session_id)  # Update session if provided
        if course_id:
            student.course_id = Course.objects.get(id=course_id)  # Update course if provided

        student.save()  # Save student updates

        messages.success(request, 'Student Updated Successfully')
        return redirect('student_list')

    return render(request, 'users/Hod/student_edit.html', {'courses': course, 'sessions': sessions})


@login_required
def STUDENT_DELETE(request, student_id):
    try:
        student = CustomUser.objects.get(id=student_id)
        student.delete()
        messages.success(request, 'Student Deleted Successfully')
        return redirect('student_list')
    except Exception as e:
        messages.error(request, 'An error occurred while deleting the student.')
        return redirect('student_delete_error')

@login_required
def TEACHER_LIST(request):
    teacher=Staff.objects.all()
    context = {'teacher':teacher}
    return render(request, 'users/Hod/teacher_list.html',context)

@login_required
def TEACHER_ADD(request):
    if request.method == 'POST':
        name = request.POST.get('name').strip()
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        mobile_no = request.POST.get('mobile_number')
        email = request.POST.get('email')
        join_date = request.POST.get('join_date')
        qualification = request.POST.get('qualification')
        experience = request.POST.get('experience')
        address = request.POST.get('address')

        if name:
            parts = name.split(' ')
            first_name = parts[0]
            last_name = parts[-1]

            # Generate initial username and teacher_id
            base_username = f"{first_name.lower()}{last_name.lower()}"
            teacher_id = f"{first_name[0].upper()}{last_name[0].upper()}{str(random.randint(100, 999))}"

            # Ensure username is unique
            username = base_username
            counter = 1
            while CustomUser.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1

            # Ensure teacher_id is unique
            while Staff.objects.filter(teacher_id=teacher_id).exists():
                teacher_id = f"{first_name[0].upper()}{last_name[0].upper()}{str(random.randint(100, 999))}"

            password = f"{name.lower()}@123"

        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request, 'Username already taken!!!')
            return redirect('teacher_add')

        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request, 'Email already taken!!!')
            return redirect('teacher_add')

        # Create and save the user
        user = CustomUser(
            first_name=name,
            last_name="VIT",
            username=username,
            email=email,
            profile_pic=None,
            user_type=2
        )
        user.set_password(password)
        user.save()

        # Create and save the staff
        staff = Staff(
            admin=user,
            name=name,
            teacher_id=teacher_id,
            gender=gender,
            date_of_birth=dob,
            phone_number=mobile_no,
            join_date=join_date,
            qualification=qualification,
            experience=experience,
            address=address
        )
        staff.save()

        # Send email with credentials
        subject = 'Your Teacher Account Credentials'
        message = f"""
                    Hi {first_name},
                    Welcome to Vidyalankar SCMS...

                    Your account has been successfully created.

                    Username: {username}
                    Password: {password}

                    Please log in to your account.

                    Best regards,
                    Team NEXGEN19
                    """
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
        except Exception as e:
            # Log the error if needed, or handle it quietly
            print(f"Error sending email: {e}")

        messages.success(request, 'Teacher Added Successfully')
        return redirect('teacher_add')

    return render(request, 'users/Hod/teacher_add.html')


@login_required
def TEACHER_EDIT(request,teacher_id):
    teacher=Staff.objects.filter(id=teacher_id)
    context = {'teacher':teacher}
    return render(request,'users/Hod/teacher_edit.html',context)


@login_required
def TEACHER_UPDATE(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        teacher_id = request.POST.get('teacher_id')
        user = get_object_or_404(CustomUser, id=id)  # Safely retrieve the user

        # Get data from the request
        name = request.POST.get('name')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        mobile_no = request.POST.get('mobile_no')
        email = request.POST.get('email')
        join_date = request.POST.get('join_date')
        qualification = request.POST.get('qualification')
        experience = request.POST.get('experience')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')

        # Update user fields only if they are provided
        if name:
            user.first_name = name
        if gender:
            user.gender = gender
        if dob:
            user.date_of_birth = dob
        if mobile_no:
            user.mobile_number = mobile_no
        if email:
            user.email = email
        if username:
            user.username = username
        if address:
            user.address = address  # Assuming 'address' is a field in CustomUser

        # Update Staff details
        try:
            staff = Staff.objects.get(admin=user)  # Assuming Staff has a one-to-one relationship with CustomUser

            if teacher_id:
                staff.teacher_id = teacher_id  # Update only if provided
            if gender:
                staff.gender = gender
            if dob:
                staff.date_of_birth = dob
            if mobile_no:
                staff.phone_number = mobile_no
            if join_date:
                staff.join_date = join_date
            if qualification:
                staff.qualification = qualification
            if experience:
                staff.experience = experience
            if address:
                staff.address = address  # Assuming 'address' is a field in Staff

            staff.save()
        except Staff.DoesNotExist:
            messages.error(request, "Staff record not found.")
            return redirect('teacher_list')

        # Save the user and handle password separately
        if password:
            user.set_password(password)

        user.save()
        messages.success(request, "Teacher updated successfully.")
        return redirect('teacher_list')

    messages.error(request, "Invalid request method.")
    return redirect('teacher_list')


@login_required
def TEACHER_DELETE(request,teacher_id):
    teacher=CustomUser.objects.get(id=teacher_id)
    teacher.delete()
    messages.success(request, 'Teacher Deleted Successfully')
    return redirect('teacher_list')

@login_required
def BRANCH_LIST(request):
    course=Course.objects.all()
    context = {'course':course}
    return render(request, 'users/Hod/branch_list.html',context)

@login_required
def BRANCH_ADD(request):
    if request.method == 'POST':
        branch_name=request.POST.get('branch_name')
        branch_id=request.POST.get('branch_id')
        branch_intake=request.POST.get('branch_intake')
        course=Course(
            name=branch_name,
            short_name=branch_id,
            intake=branch_intake

        )
        course.save()
        messages.success(request, 'Branch Added Successfully')
        return redirect('branch_add')

    return render(request,'users/Hod/branch_add.html')

@login_required
def BRANCH_DELETE(request,branch_id):
    branch=Course.objects.get(id=branch_id)
    branch.delete()
    messages.success(request, 'Branch Deleted Successfully')
    return redirect('branch_list')

@login_required
def SUBJECT_ADD(request):
    branches=Course.objects.all()
    teachers=Staff.objects.all()
    context={'branches':branches,'teachers':teachers}
    if request.method == 'POST':
        subject_name=request.POST.get('subject_name')
        subject_id=request.POST.get('subject_id')
        teacher_id=request.POST.get('teacher_id')
        branch_id=request.POST.get('branch_id')
        subject_credits=request.POST.get('subject_credits')
        semester=request.POST.get('semester')
        teacher=Staff.objects.get(teacher_id=teacher_id)
        branch=Course.objects.get(short_name=branch_id)
        subject=Subjects(
            name=subject_name,
            subject_id=subject_id,
            semester=semester,
            credits=subject_credits,
            teacher_id=teacher,
            course_id=branch
        )
        subject.save()
        messages.success(request, 'Subject Added Successfully')
    else:
        messages.error(request, 'No Subject Selected')
    return render(request,'users/Hod/subject_add.html',context)

@login_required
def SUBJECT_LIST(request):
    subjects=Subjects.objects.all()
    context={'subjects':subjects}
    return render(request,'users/Hod/subject_list.html',context)

@login_required
def HOLIDAYS(request):
    holidays=Holidays.objects.all()
    context={'holidays':holidays}
    return render(request,'users/Hod/holiday.html',context)

@login_required
def HOLIDAY_ADD(request):
    if request.method == 'POST':
        name=request.POST.get('name')
        type=request.POST.get('type')
        start=request.POST.get('start')
        end=request.POST.get('end')
        holiday=Holidays(
            name=name,
            holiday_type=type,
            start_date=start,
            end_date=end
        )
        holiday.save()
        messages.success(request, 'Holiday Added Successfully')
        return redirect('holidays')
    return render(request,'users/Hod/holiday_add.html')

@login_required
def HOLIDAY_DELETE(request,holiday_id):
    holiday=Holidays.objects.get(id=holiday_id)
    holiday.delete()
    messages.success(request, 'Holiday Deleted Successfully')
    return redirect('holidays')


def EVENTS(request):
    if request.user.user_type == '1':
        base_template = 'users/base.html'
    elif request.user.user_type == '2':
        base_template = 'users/base3.html'
    else:
        base_template = 'users/base2.html'
    return render(request,'users/Hod/events.html',{
        'base_template': base_template,
        'user': request.user,
    })


def TIMETABLE_ADD(request):
    branches=Course.objects.all()
    if request.method == 'POST':
        short_name=request.POST.get('branch')
        semester=request.POST.get('semester')
        course=Course.objects.get(short_name=short_name)
        rooms=Room.objects.all()
        timetable = Timetable.objects.filter(branch__short_name=short_name, semester=int(semester))
        semesters="SEM-"+semester
        subjects = Subjects.objects.filter(course_id=course, semester=semesters)
        context={'timetable':timetable,'short_name':short_name,'semester':semester,'subjects':subjects,'rooms':rooms}
        return render(request, 'users/Hod/timetable.html', context)

    context={'branches':branches}
    return render(request,'users/Hod/timetable_add.html',context)



def TIMETABLE_FILTER(request):
    day = request.GET.get('day')
    short_name = request.GET.get('branch')
    semester = request.GET.get('sem')
    course = Course.objects.get(short_name=short_name)
    subjects = Subjects.objects.filter(course_id=course)
    rooms = Room.objects.all()
    if day is not None:
        timetable = Timetable.objects.filter(branch__short_name=short_name, semester=int(semester),day=day)
    else:
        timetable = Timetable.objects.filter(branch__short_name=short_name,semester=int(semester))
    context={'timetable':timetable,'short_name':short_name,'semester':semester,'subjects':subjects,'rooms':rooms}
    return render(request, 'users/Hod/timetable.html', context)


def TIMETABLE_DELETE(request,timetable_id):
    timetable=Timetable.objects.get(timetable_id=timetable_id)
    timetable.delete()
    messages.success(request, 'Timetable Deleted Successfully')
    return redirect('timetableadd')


def FEES(request):
    fees=Fess.objects.all()
    context={'fees':fees}

    return render(request,'users/Hod/fees.html',context)

def check_schedule_conflict(request):
    if request.method == 'GET':
        day = request.GET.get('day')
        start_time = request.GET.get('start_time')
        teacher_id = request.GET.get('teacher_id')
        room = request.GET.get('room')
        print(day,start_time,teacher_id,room)
        # Check for conflicts
        conflicts = Timetable.objects.filter(
            day=day,
            teacher_id=teacher_id,
            start_time=start_time,
            room=room
        ).exists()

        return JsonResponse({'conflict': conflicts})


def ADD_SLOT(request):
    if request.method == 'POST':
        subject_id=request.POST.get('subject_id')
        day=request.POST.get('day')
        start_time=request.POST.get('start_time')
        teacher_id=request.POST.get('teacher_id')
        room_number = request.POST.get('room_number')
        lab_theory=request.POST.get('lab_theory')
        short_name=request.POST.get('branch')
        semester=request.POST.get('semester')
        start_time_dt = datetime.strptime(start_time, '%H:%M')
        end_time_dt = start_time_dt + timedelta(hours=2)
        start_time_12hr = start_time_dt.strftime('%I:%M %p')  # 12-hour format with AM/PM
        end_time_12hr = end_time_dt.strftime('%I:%M %p')
        print(short_name)
        subject = Subjects.objects.get(subject_id=subject_id)
        teacher=Staff.objects.get(teacher_id=teacher_id)
        room = Room.objects.get(room_number=room_number)
        course = get_object_or_404(Course, short_name=short_name)
        print

        timetable=Timetable(
            subject_name=subject,
            day=day,
            start_time=start_time_dt,
            end_time=end_time_dt,
            teacher_id=teacher,
            room_no=room,
            lab_or_theory=lab_theory,
            semester=semester,
            branch=course
        )
        timetable.save()
        timetable = Timetable.objects.filter(branch__short_name=short_name, semester=int(semester))
        rooms=Room.objects.all()
        subjects=Subjects.objects.filter(course_id=course, semester=semester)
        messages.success(request, 'Added Successfully')
        context = {'timetable': timetable, 'short_name': short_name, 'semester': semester, 'subjects': subjects,
                   'rooms': rooms}
        return render(request, 'users/Hod/timetable.html', context)


def BRANCH_EDIT(request,branch_name):
    branch=Course.objects.get(short_name=branch_name)
    context={'branch':branch}
    if request.method == 'POST':
        branch_name=request.POST.get('branch_name')
        branch_id=request.POST.get('branch_id')
        branch_intake=request.POST.get('branch_intake')

        if branch_name:
            branch.name=branch_name
        if branch_id:
            branch.short_name=branch_id
        if branch_intake:
            branch.intake=branch_intake
        branch.save()
        messages.success(request, 'Branch Edited Successfully')
        return redirect('branch_list')
    return render(request,'users/Hod/branch_edit.html',context)


def SUBJECT_EDIT(request,subject_id):
    return None


def STUDENT_SEARCH(request):
    search_query = request.GET.get('search')
    search_by = request.GET.get('search_by')
    students = Student.objects.all()  # Initialize with all students

    if search_query and search_by:
        if search_by.lower() == 'id':  # Make search_by case-insensitive
            students = Student.objects.filter(student_id__icontains=search_query)
        elif search_by.lower() == 'name':
            students = Student.objects.filter(
                Q(admin__first_name__icontains=search_query) |
                Q(admin__last_name__icontains=search_query)
            )

    context = {'students': students}
    return render(request, 'users/Hod/student_list.html', context)


def SUBJECT_FILTER(request):
    subjects = []  # Default to an empty list

    if request.method == 'POST':
        query1 = request.POST.get('query1')
        query2 = request.POST.get('query2')
        query2="SEM-"+query2

        if query1 and query2:  # Check that both queries are provided
            subjects = Subjects.objects.filter(course_id__name=query1, semester=query2)

    context = {'subjects': subjects}
    return render(request, 'users/Hod/subject_list.html', context)


def STUDENT_PROFILE(request,student_id):
    student = Student.objects.get(student_id=student_id)
    return render(request, 'users/Hod/student_profile.html', {'student': student})


def create_event(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        start = request.POST.get('start')
        end = request.POST.get('end')
        all_day = request.POST.get('all_day') == 'on'  # Checkbox returns 'on' if checked

        # Create the event
        event = Event(title=title, start=start, end=end if end else None, all_day=all_day)
        event.save()
        messages.success(request, 'Event Created')

        # Optionally redirect to the events page or render a success message
        return redirect('events')  # Change this to your events page URL

    # If not POST, redirect or render a page
    return redirect('events')  # Change as needed


def EXAM_LIST(request):
    exams = Exam_Schedule.objects.select_related('Branch', 'subject').all()
    branches = Course.objects.all()  # Assuming Course is your branch model
    subjects = Subjects.objects.all()
    return render(request, 'users/Hod/exam_list.html', {
        'exams': exams,
        'branches': branches,
        'subjects': subjects,
    })



def create_exam_schedule(request):
    if request.method == 'POST':
        name = request.POST['name']
        branch = Course.objects.get(id=request.POST['branch'])
        subject = Subjects.objects.get(subject_id=request.POST['subject'])
        semester = request.POST['semester']
        date = request.POST['date']
        start_time = request.POST['start_time']
        exam_type = request.POST['exam_type']

        exam_schedule = Exam_Schedule(
            name=name,
            Branch=branch,
            subject=subject,
            semester=semester,
            date=date,
            start_time=start_time,
            exam_type=exam_type
        )
        exam_schedule.save()
        messages.success(request, 'Shedule Added Sucessfully')
        return redirect('exam_list')  # Adjust redirect as necessary

def delete_exam_schedule(request, id):
    exam_schedule = get_object_or_404(Exam_Schedule, id=id)
    exam_schedule.delete()
    messages.success(request,'Shedule Deleted Sucessfully')
    return redirect('exam_list')