from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from users.models import Student,CustomUser,Course,Session_Year,Staff,Subjects,Holidays,Timetable,Room,Registration,Assignment,Submission,Note,Results,Notification
from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse
from datetime import datetime, timedelta
import random
from django.db.models import Q
import os
from django.conf import settings




def HOME(request):
    user=request.user.username
    teacher=Staff.objects.get(admin__username=user)
    upcoming_classes = Timetable.objects.filter(teacher_id=teacher).order_by('start_time')
    context={'upcoming_classes':upcoming_classes}
    return render(request,'users/Staff/Home.html',context)



# def upload_note(request):
#     if request.method == 'POST':
#         title = request.POST.get('title')
#         subject_id = request.POST.get('subject')
#         note_type = request.POST.get('note_type')
#         file = request.FILES.get('file')
#
#         if title and subject_id and note_type and file:
#             subject = Subject.objects.get(id=subject_id)
#
#             # Create a folder for the subject if it doesn't exist
#             subject_folder = f'notes/{subject.name}/'
#             note = Note(title=title, file=file, subject=subject, teacher=request.user, note_type=note_type)
#             note.file.name = f"{subject_folder}{file.name}"
#             note.save()
#             return redirect('note_list')
#         else:
#             return HttpResponse("Invalid data", status=400)
#
#     subjects = Subject.objects.all()
#     return render(request, 'upload_note.html', {'subjects': subjects})


def STUDENT_LIST(request):
    username=request.user.username
    teacher=Staff.objects.get(admin__username=username)
    subjects=Subjects.objects.filter(teacher_id=teacher)
    sem = subjects.first().semester.split()[-1]
    sem=sem[-1]
    print(sem)
    register=Registration.objects.filter(semester=int(sem))
    context={'register':register}
    return render(request,'users/Staff/Student_List.html',context)


def ASSIGNMENT_UPLOAD(request):
    if request.method == "POST":
        name=request.POST['name']
        points=request.POST['points']
        desc=request.POST['desc']
        due=request.POST['due']
        file=request.FILES['file']
        username=request.user.username
        teacher = Staff.objects.get(admin__username=username)
        subjects = Subjects.objects.filter(teacher_id=teacher).first()

        assignment=Assignment(title=name,description=desc,points=points,subject_id=subjects,course_id=subjects.course_id,file=file,due_date=due,uploaded_by=teacher)
        assignment.save()
        messages.success(request,'Assignment has been successfully uploaded')
    return render(request,'users/Staff/upload_assignment.html')


def ASSIGNMENT_SUBS(request):
    username = request.user.username
    teacher = Staff.objects.get(admin__username=username)
    subjects = Subjects.objects.filter(teacher_id=teacher).first()
    submissions=Submission.objects.filter(assignment__subject_id=subjects)
    context={'submissions':submissions}
    if request.method == "POST":
        assignment_id = request.POST.get('submission_id')
        points=request.POST['points']
        submission=Submission.objects.get(id=assignment_id)
        submission.feedback=points
        submission.save()
        messages.success(request,'Returned Sucessfully')
        return redirect('assignment_submission')

    return render(request,'users/Staff/submissions.html',context)


def ASSIGNMENTS_UPLOADED(request):
    username = request.user.username
    teacher = Staff.objects.get(admin__username=username)
    assingnments=Assignment.objects.filter(uploaded_by=teacher)
    context={'assingnments':assingnments}
    return render(request,'users/Staff/assignments.html',context)


def ASSIGNMENT_DELETE(request, assignment_id):
    try:
        # Get the assignment object
        assignment = Assignment.objects.get(id=assignment_id)

        # Check if the assignment has a file and delete it
        if assignment.file:  # Assuming the file field is named 'file'
            file_path = os.path.join(settings.MEDIA_ROOT, str(assignment.file))  # Get the full file path
            if os.path.isfile(file_path):  # Check if the file exists
                os.remove(file_path)  # Delete the file

        # Now delete the assignment record
        assignment.delete()

        messages.success(request, 'Assignment has been deleted')
    except Assignment.DoesNotExist:
        messages.error(request, 'Assignment not found')
    except Exception as e:
        messages.error(request, f'Error occurred: {str(e)}')

    return redirect('uploaded_assignments')


def UPLOAD_NOTES(request):
    if request.method == "POST":
        title=request.POST['title']
        file=request.FILES['file']
        type=request.POST['type']
        username = request.user.username
        teacher = Staff.objects.get(admin__username=username)
        subjects = Subjects.objects.filter(teacher_id=teacher).first()

        print(title,file,type,teacher,subjects)

        note=Note(title=title,file=file,note_type=type,teacher=teacher,subject=subjects)
        note.save()
        messages.success(request,'Note has been uploaded')
        return redirect('upload_notes')

    return render(request,'users/Staff/notes_upload.html')


def UPLOADED_NOTES(request):
    username = request.user.username
    teacher = Staff.objects.get(admin__username=username)
    notes=Note.objects.filter(teacher=teacher)
    context={'notes':notes}
    return render(request,'users/Staff/uploaded_notes.html',context)


def UPLOAD_NOTES_DELETE(request, note_id):
    try:
        # Get the note object
        note = Note.objects.get(id=note_id)

        # Check if the note has a file and delete it
        if note.file:  # Assuming the file field is named 'file'
            file_path = os.path.join(settings.MEDIA_ROOT, str(note.file))  # Get the full file path
            if os.path.isfile(file_path):  # Check if the file exists
                os.remove(file_path)  # Delete the file

        # Now delete the note record
        note.delete()

        messages.success(request, 'Note has been deleted')
    except Note.DoesNotExist:
        messages.error(request, 'Note not found')
    except Exception as e:
        messages.error(request, f'Error occurred: {str(e)}')

    return redirect('uploaded_notes')







def RESULTS(request):
    username = request.user.username
    teacher = get_object_or_404(Staff, admin__username=username)
    subjects = Subjects.objects.filter(teacher_id=teacher)
    # print(subjects,teacher)

    # Get current semester
    sem = subjects.first().semester if subjects.exists() else None
    # print(sem)
    if not sem:
        messages.error(request, "No subjects found for this teacher.")
        return redirect('some_error_page')

    # Extract semester number
    try:
        sem_number = int(sem.split('-')[1])  # e.g., "SEM-1" -> 1
    except (IndexError, ValueError):
        messages.error(request, "Unable to determine semester.")
        return redirect('some_error_page')

    # Get all registrations for that semester
    registrations = Registration.objects.filter(semester=sem_number)
    # print(registrations)

    # Create a dictionary to hold results by student ID
    results_dict = {result.student.admin.username: result for result in Results.objects.filter(subject__in=subjects)}
    print(results_dict)

    # Prepare the context, pairing each registration with its result if it exists
    context = []
    for reg in registrations:
        username = reg.student_id.admin.username  # Get the username of the student
        print(f"Checking for Username: {username}")  # Debug print
        result = results_dict.get(username)  # Attempt to retrieve the result using username

        if result:
            print(f"Found Result: {result}")  # Debug print
        else:
            print("No result found for this student.")  # Debug print

        context.append({
            'student': reg.student_id,
            'result': result
        })
    print(context)

    # Handle form submission for saving marks
    if request.method == "POST":
        student_id = request.POST.get('student_id')
        isa = request.POST.get('isa')
        mse = request.POST.get('mse')
        ese = request.POST.get('ese')

        subject = subjects.first()  # Assuming you want the first subject for the teacher
        if subject:
            try:
                student = Student.objects.get(student_id=student_id)

                # Update existing result or create a new one
                result, created = Results.objects.update_or_create(
                    student=student,
                    subject=subject,
                    defaults={
                        'isa_marks': isa,
                        'mse_marks': mse,
                        'ese_marks': ese
                    }
                )

                # Calculate total marks
                result.total_marks = (result.isa_marks or 0) + (result.mse_marks or 0) + (result.ese_marks or 0)
                result.save()  # Save total marks

                if created:
                    messages.success(request, 'Result has been created.')
                else:
                    messages.success(request, 'Result has been updated.')

                return JsonResponse({'success': True})
            except Student.DoesNotExist:
                messages.error(request, "Student not found.")
        else:
            messages.error(request, "Subject not found.")

    return render(request, 'users/Staff/results.html', {'context': context})

import csv
def RESULTS_DOWNLOAD(request):
    user=request.user.username
    teacher = get_object_or_404(Staff, admin__username=user)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="results.csv"'

    writer = csv.writer(response)
    # Write the header row
    writer.writerow(['ID', 'First Name','Last Name', 'Subject', 'ISA', 'MSE', 'ESE'])

    # Fetch results data
    results = Results.objects.filter(uploaded_by=teacher)  # Adjust based on your filtering needs

    for subject in results:
        writer.writerow([
            subject.student.student_id,
            subject.student.admin.first_name,
            subject.student.admin.last_name,
            subject.subject.name,
            subject.isa_marks,
            subject.mse_marks,
            subject.ese_marks,
        ])
    return response


# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@require_POST  # Ensure this view only handles POST requests
def reschedule_lesson(request):
    timetable_id = request.POST.get('timetable_id')
    new_date = request.POST.get('new_date')
    new_time = request.POST.get('new_time')

    # Logic to update the lesson in your database
    # Example: Lesson.objects.filter(id=timetable_id).update(date=new_date, time=new_time)

    # Create a notification
    notification_message = f'Lesson {timetable_id} rescheduled to {new_date} at {new_time}.'
    Notification.objects.create(message=notification_message)

    # Redirect or return a response
    return redirect('dashboard')
