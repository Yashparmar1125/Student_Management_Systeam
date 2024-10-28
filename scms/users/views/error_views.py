from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from users.models import Student,CustomUser,Course,Session_Year,Staff,Subjects,Holidays,Registration,Assignment,Submission
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
import os
from django.conf import settings


def REGISTRATION_ERROR(request):
    return render(request, 'users/registeration_error.html')


def STUDENT_DELETE_ERROR(request):
    return render(request, 'users/student_delete_error.html')