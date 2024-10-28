from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from users.models import CustomUser,Student,Staff,Course,Fess,Event
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from users.EmailBackend import EmailBackend
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
import string,random


def BASE(request):
    return render(request, 'users/base.html')


def LOGIN(request):
    return render(request, 'users/login.html')

def doLogin(request):
    if request.method == 'POST':
        user=EmailBackend.authenticate(request,username=request.POST.get('email'),password=request.POST.get('password'))
        if user!=None:
            login(request,user)
            user_type=user.user_type
            if user_type=='1':
                return redirect('hod_home')
            elif user_type=='2':
                return redirect('teacher_home')
            elif user_type=='3':
                return redirect('student_home')
            else:
                messages.error(request,'Invalid Email or Password')
                return redirect('login')

        else:
            messages.error(request, 'Invalid Email or Password')
            return redirect('login')

@login_required(login_url='/')
def doLogout(request):
    logout(request)
    return redirect('login')


@login_required(login_url='/')
def PROFILE(request):
    if request.user.user_type == '1':
        base_template = 'users/base.html'
    elif request.user.user_type == '2':
        base_template = 'users/base3.html'
    else:
        base_template = 'users/base2.html'

    return render(request, 'users/profile_view.html', {
        'base_template': base_template,
        'user': request.user,
    })


@login_required(login_url='/')
def UPDATE_PROFILE(request):
    if request.user.user_type == '1':
        base_template = 'users/base.html'
    elif request.user.user_type == '2':
        base_template = 'users/base3.html'
    else:
        base_template = 'users/base2.html'

    return render(request, 'users/profile.html', {
        'base_template': base_template,
        'user': request.user,
    })

@login_required(login_url='/')
def doUpdate(request):
    if request.user.user_type == '1':
        base_template = 'users/base.html'
    elif request.user.user_type == '2':
        base_template = 'users/base3.html'
    else:
        base_template = 'users/base2.html'
    if request.method == 'POST':
        profile_pic=request.FILES.get('profile_pic')
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        dob=request.POST.get('dob')
        mobile=request.POST.get('mob_num')
        address=request.POST.get('address')

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            if profile_pic != None and profile_pic != "":
                customuser.profile_pic = profile_pic
            customuser.first_name=first_name
            customuser.last_name=last_name
            customuser.mobile_number=mobile
            customuser.Address=address
            customuser.save()
            messages.success(request, 'Profile Updated Successfully')
            print(customuser.profile_pic)
            return redirect('doUpdate')
        except:
            messages.error(request, 'Unable to Update Profile')
            return redirect('doUpdate')

    return render(request, 'users/profile_view.html',{
        'base_template': base_template,
        'user': request.user,
    })

@login_required
def Dashboard(request):
    student_number = Student.objects.count()
    departments_number = Course.objects.count()
    teacher_number = Staff.objects.count()
    context = {'student_number': student_number, 'departments_number': departments_number,
               'teacher_number': teacher_number}
    if request.user.user_type=='1':
        return redirect('hod_home')
    if request.user.user_type=='2':
        return redirect('teacher_home')
    else:
        return redirect('student_home')


@login_required
def changePassword(request):
    if request.method == 'POST':
        old_password=request.POST.get('old_password')
        new_password=request.POST.get('new_password')
        conf_password=request.POST.get('conf_password')
        if check_password(old_password, request.user.password):
            # Check if new password and confirm password match
            if new_password == conf_password:
                # Set the new password
                request.user.set_password(new_password)
                request.user.save()

                # Update session to prevent logout
                update_session_auth_hash(request, request.user)

                messages.success(request, 'Your password has been updated successfully!')
                return redirect('profile')  # Redirect to profile or any page after success
            else:
                messages.error(request, 'New password and confirm password do not match.')
        else:
            messages.error(request, 'Old password is incorrect.')

        return render(request, 'profile_view.html')


def MAINTAINENCE(request):
    return render(request, 'maintainence_error.html')


import random
from django.http import JsonResponse


def chart_data(request):
    # Check if attendance data is already stored in the session
    if 'attendance' not in request.session:
        # Generate unique attendance data for the user
        attendance = [random.randint(50, 100) for _ in range(7)]
        # Store the generated data in the session
        request.session['attendance'] = attendance

    # Retrieve attendance data from the session
    attendance = request.session['attendance']

    data = {
        "attendance": attendance
    }

    return JsonResponse(data)


def Payments_Gateway(request):
    if request.method=='POST':
        student_id=request.POST.get('student_id')
        student=Student.objects.get(student_id=student_id)
        semester=request.POST.get('semester')
        amount=request.POST.get('amount')
        comment=request.POST.get('comments')
        payment_method=request.POST.get('payment_method')

        characters = string.ascii_letters + string.digits + string.punctuation
        transaction_id = ''.join(random.choice(characters) for _ in range(12))

        fess=Fess(transaction_id=transaction_id,student=student,semester=semester,amount=amount,description=comment,mode=payment_method)
        fess.save()
        messages.success(request, 'Payment Successful')
    return render(request, 'users/paymets_gateway.html')


def Sucess_Payments_Gateway(request):
    return render(request, 'users/successPage.html')

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .serializers import EventSerializer
import json

@csrf_exempt
def event_list(request):
    if request.method == "GET":
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == "POST":
        data = json.loads(request.body)
        event = Event.objects.create(**data)
        return JsonResponse(EventSerializer(event).data, status=201)

@csrf_exempt
def event_detail(request, pk):
    try:
        event = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        return JsonResponse({"error": "Event not found"}, status=404)

    if request.method == "DELETE":
        event.delete()
        return JsonResponse({"message": "Event deleted"}, status=204)

    elif request.method == "PUT":
        data = json.loads(request.body)
        for attr, value in data.items():
            setattr(event, attr, value)
        event.save()
        return JsonResponse(EventSerializer(event).data)
