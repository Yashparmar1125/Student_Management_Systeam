from lib2to3.fixes.fix_input import context

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from users.models import Student,CustomUser,Course,Session_Year,Staff,Subjects,Holidays,Registration,Assignment,Submission,Timetable,Room,Note,Results,Fess,Exam_Schedule
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
import os
from django.conf import settings


def HOME(request):
    context = {
        'timetable': None,
        'timetables': None,
        'subjects': None,
        'results': None,
    }

    try:
        username = request.user.username
        student = Student.objects.get(admin__username=username)
        register = Registration.objects.get(student_id=student)

        # Fetch timetable
        timetable = Timetable.objects.filter(branch=student.course_id, semester=register.semester)[:2]
        timetables = Timetable.objects.filter(branch=student.course_id, semester=register.semester)[:4]

        subjects = Subjects.objects.filter(
            semester=f"SEM-{register.semester}",
            course_id=student.course_id
        ).count()

        results=Results.objects.filter(student_id=student).count()

        context['timetable'] = timetable
        context['timetables'] = timetables
        context['subjects'] = subjects
        context['results'] = results

    except Student.DoesNotExist:
        print("Student not found")
    except Registration.DoesNotExist:
        print("Registration not found")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    print(context['timetable'])

    return render(request, 'users/Student/Home.html', context)


def REGISTRATION(request):
    if request.method == 'POST':
        semester = request.POST.get('semester')
        username = request.user.username

        try:
            student = Student.objects.get(admin__username=username)
        except Student.DoesNotExist:
            messages.error(request, 'Student record not found.')
            return redirect('register_student')

        if Registration.objects.filter(semester=semester, student_id=student).exists():
            messages.warning(request, 'You have already registered for this semester.')
            return redirect('register_student')

        try:
            registration = Registration(
                student_id=student,
                semester=semester
            )
            registration.save()
            messages.success(request, 'Registration successful')
        except Exception as e:
            messages.error(request, f'An error occurred while registering: {str(e)}')
            return redirect('register_student')

        return redirect('register_student')

    return render(request, 'users/Student/Registration.html')


def SUBJECTS(request):
    username = request.user.username

    try:
        student = Student.objects.get(admin__username=username)
    except Student.DoesNotExist:
        messages.error(request, 'Student record not found.')
        return redirect('registration_error')  # Redirect to an appropriate view

    try:
        registration = Registration.objects.get(student_id=student)
    except Registration.DoesNotExist:
        messages.error(request, 'Registration record not found.')
        return redirect('registration_error')  # Redirect to an appropriate view

    subjects = Subjects.objects.filter(
        semester=f"SEM-{registration.semester}",
        course_id=student.course_id
    )

    return render(request, 'users/Student/Subjects.html', {'subjects': subjects})



def ASSIGNMENTS_UPCOMMING(request):
    username = request.user.username
    student = Student.objects.get(admin__username=username)

    # Get the current date and time
    type = "Upcoming"
    now = timezone.now()

    # Filter assignments where the due date is greater than the current date
    # and the student has not submitted that assignment
    assignments = Assignment.objects.filter(
        course_id=student.course_id,
        due_date__gt=now
    ).exclude(
        submission__student=student
    )

    context = {'assignments': assignments, 'type': type}
    return render(request, 'users/Student/assignments.html', context)



def ASSIGNMENTS_PAST_DUE(request):
    username = request.user.username
    student = Student.objects.get(admin__username=username)
    type = "Past Due"

    # Get the current date and time
    now = timezone.now()

    # Filter past due assignments that have not been submitted by the student
    assignments = Assignment.objects.filter(
        course_id=student.course_id,
        due_date__lt=now  # Only assignments that are past their due date
    ).exclude(
        submission__student=student  # Exclude assignments submitted by this student
    )

    context = {'assignments': assignments,'type': type}
    return render(request, 'users/Student/assignments.html', context)


def ASSIGNMENTS_SUBMITTED(request):
    username = request.user.username
    type="Submitted"
    student = Student.objects.get(admin__username=username)

    # Retrieve all submissions for the logged-in student
    assignments = Submission.objects.filter(student=student)

    context = {'assignments': assignments,'type': type}
    return render(request, 'users/Student/assignments.html', context)


def ASSIGNMENT_UPLOAD(request):
    if request.method == 'POST':
        assignment_id = request.POST.get('assignment_id')
        uploaded_file = request.FILES.get('file')
        print(assignment_id,uploaded_file)

        # Check if the assignment ID and uploaded file are provided
        if not assignment_id:
            messages.error(request, 'Assignment ID not provided.')
            return redirect('assignments_submitted')

        if not uploaded_file:
            messages.error(request, 'No file uploaded.')
            return redirect('assignments_submitted')

        try:
            # Try to fetch the assignment
            assignment = Assignment.objects.filter(id=assignment_id).first()

            # If assignment not found, check if there's an existing submission for this assignment
            if not assignment:
                submission = Submission.objects.filter(assignment__id=assignment_id, student__admin__username=request.user.username).first()
                if submission:
                    messages.error(request, 'You have already submitted this assignment.')
                    return redirect('assignments_submitted')
                else:
                    messages.error(request, 'Assignment not found and no prior submission exists.')
                    return redirect('assignments_submitted')

            # Fetch the student
            student = get_object_or_404(Student, admin__username=request.user.username)

            # Create and save the submission
            submission = Submission(
                assignment=assignment,
                student=student,
                file=uploaded_file
            )
            submission.save()

            messages.success(request, 'Assignment uploaded successfully')

        except ObjectDoesNotExist:
            messages.error(request, 'An unexpected error occurred.')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')

        # Always redirect after processing
        return redirect('assignments_submitted')

    # Handle case when request is not POST
    messages.error(request, 'Invalid request method.')
    return redirect('assignments_submitted')

def ASSIGNMENT_UNDO_UPLOAD(request):
    assignment_id = request.GET.get('assignment_id')
    print(assignment_id)

    # Retrieve the submission
    submission = get_object_or_404(Submission, assignment__id=assignment_id,
                                   student__admin__username=request.user.username)

    # Delete the uploaded file if it exists
    if submission.file:
        file_path = os.path.join(settings.MEDIA_ROOT, submission.file.name)
        if os.path.isfile(file_path):
            os.remove(file_path)

    # Delete the submission
    submission.delete()
    messages.success(request, 'Upload successfully undone.')
    return redirect('assignments_submitted')



def HOLIDAYS(request):
    holidays=Holidays.objects.all()
    context={'holidays':holidays}
    return render(request,'users/Student/holidays.html',context)


def TIMETABLE(request):
    user=request.user.username
    student=Student.objects.get(admin__username=user)
    short_name=student.course_id.short_name
    register=Registration.objects.get(student_id=student)
    semester=register.semester
    print(short_name,semester)
    course = Course.objects.get(short_name=short_name)
    timetable = Timetable.objects.filter(branch__short_name=short_name, semester=int(semester))
    context = {'timetable': timetable, 'short_name': short_name, 'semester': semester,
               }
    return render(request, 'users/Student/timetable.html',context)


def RESULTS(request):
    user=request.user.username
    student=Student.objects.get(admin__username=user)
    print(student)
    results=Results.objects.filter(student=student)
    print(results)
    context={'results':results}

    return render(request, 'users/Student/results.html',context)


def EVENTS():
    return None


def SUBJECT_NOTES(request):
    username = request.user.username

    # Retrieve the student object
    student = get_object_or_404(Student, admin__username=username)

    # Get the student's current semester from the Registration model
    registration = get_object_or_404(Registration, student_id=student)

    # Get the student's subject based on their course
    subjects = Subjects.objects.filter(course_id=student.course_id)

    # Find notes related to the student's subjects
    notes = Note.objects.filter(subject__in=subjects,note_type='subject_note')
    context={'notes':notes}

    return render(request, 'users/Student/subject_notes.html',context)


def PRACTISE_PAPERS(request):
    username = request.user.username

    # Retrieve the student object
    student = get_object_or_404(Student, admin__username=username)

    # Get the student's current semester from the Registration model
    registration = get_object_or_404(Registration, student_id=student)

    # Get the student's subject based on their course
    subjects = Subjects.objects.filter(course_id=student.course_id)

    # Find notes related to the student's subjects
    notes = Note.objects.filter(subject__in=subjects, note_type='practice_paper')
    context = {'notes': notes}

    return render(request, 'users/Student/subject_notes.html', context)


def PAY_FEES(request):
    username = request.user.username
    student = get_object_or_404(Student, admin__username=username)
    context = {'student': student}
    return render(request, 'users/Student/pay_fess.html',context)


def VIEW_RECIPES(request):
    username = request.user.username
    student = get_object_or_404(Student, admin__username=username)
    fess=Fess.objects.filter(student=student)
    context={'fess':fess}

    return render(request, 'users/Student/fess_list.html',context)

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer


def generate_fee_receipt(request, fee_id):
    # Retrieve the fee record
    fee = get_object_or_404(Fess, fee_id=fee_id)

    # Create the response object with the appropriate PDF header
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="fee_receipt_{fee.fee_id}.pdf"'

    # Create the PDF document
    doc = SimpleDocTemplate(response, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Header: Institute Name
    header = Paragraph("Vidyalankar Institute Of Technology", styles['Heading1'])
    story.append(header)
    story.append(Spacer(1, 12))

    # Title
    title = Paragraph("College Fee Receipt", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 12))

    # Fee details
    details = [
        f"Fee ID: {fee.fee_id}",
        f"Student Name: {fee.student.admin.first_name} {fee.student.admin.last_name}",
        f"Semester: {fee.semester}",
        f"Description: {fee.description}",
        f"Amount: ₹{fee.amount:.2f}",
        f"Mode of Payment: {fee.mode}",
        f"Paid At: {fee.paid_at.strftime('%Y-%m-%d %H:%M')}",
    ]

    for detail in details:
        p = Paragraph(detail, styles['Normal'])
        story.append(p)
        story.append(Spacer(1, 12))

    # Add a border
    border = canvas.Canvas(response)
    border.setStrokeColor(colors.black)
    border.setLineWidth(1)
    border.rect(50, 50, 500, 730, stroke=True, fill=False)

    # Build the PDF
    doc.build(story)

    return response
import csv
from django.http import HttpResponse


def download_results(request):
    username = request.user.username
    student = get_object_or_404(Student, admin__username=username)
    # Create the HttpResponse object with the appropriate CSV header
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="results.csv"'

    writer = csv.writer(response)
    # Write the header row
    writer.writerow(['ID', 'Name', 'Teacher', 'ISA', 'MSE', 'ESE'])

    # Fetch results data
    results = Results.objects.filter(student=student)  # Adjust based on your filtering needs

    for subject in results:
        writer.writerow([
            subject.id,
            subject.subject.name,
            subject.subject.teacher_id.name,
            subject.isa_marks,
            subject.mse_marks,
            subject.ese_marks,
        ])

    return response


def EXAM_LIST(request):
    user=request.user.username
    student=Student.objects.get(admin__username=user)
    register=Registration.objects.get(student_id__admin__username=user)
    exams=Exam_Schedule.objects.filter(semester=register.semester,Branch=student.course_id)
    print(exams)
    contex={'exams':exams}
    return render(request,'users/Student/exam_list.html',contex)