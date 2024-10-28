from django.shortcuts import render, redirect
from django.http import JsonResponse, StreamingHttpResponse
from .models import Person, Attendance, ImageDataset
import cv2
import numpy as np
import csv
import os
from datetime import date

def home(request):
    data = Person.objects.all()
    return render(request, 'index.html', {'data': data})

def add_person(request):
    if request.method == 'POST':
        prsnbr = request.POST.get('txtnbr')
        prsname = request.POST.get('txtname')
        prsskill = request.POST.get('optskill')
        Person.objects.create(prs_nbr=prsnbr, prs_name=prsname, prs_skill=prsskill)
        return redirect('home')
    return render(request, 'addprsn.html')

from django.http import StreamingHttpResponse
import cv2
from datetime import date
from utils.db_utils import execute_query, commit_changes

def face_recognition():
    def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, clf):
        # Your existing draw_boundary logic here
        return img

    # Initialize variables
    global justscanned, pause_cnt, cnt
    justscanned, pause_cnt, cnt = False, 0, 0

    # Load classifier
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('trained_model.yml')  # Ensure this path is correct

    # Initialize video capture
    video_capture = cv2.VideoCapture(0)

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        # Apply face recognition
        frame = draw_boundary(frame, face_cascade, scaleFactor=1.1, minNeighbors=5, color=(0, 255, 0), clf=recognizer)

        # Encode and yield the processed frame for streaming
        frame = cv2.imencode('.jpg', frame)[1].tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

    video_capture.release()
    cv2.destroyAllWindows()

def video_feed(request):
    return StreamingHttpResponse(face_recognition(), content_type='multipart/x-mixed-replace; boundary=frame')


def video_feed(request):
    return StreamingHttpResponse(face_recognition(), content_type='multipart/x-mixed-replace; boundary=frame')
