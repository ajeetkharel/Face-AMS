from django.shortcuts import render
from django.http.response import StreamingHttpResponse
from django.views.decorators import gzip

from account.models import Student
from school.models import *

import cv2

def admin_dashboard(request):
    students = Student.objects.all()
    classes = Class.objects.all()
    subjects = Subject.objects.all()
    routines = Routine.objects.all()
    attendances = Attendance.objects.all()


    context = {
        'title': "Admin Dashboard",
        'classes': classes,
    }
    return render(request, "admin_dashboard/index.html", context=context)


def register_student(request):
    return render(request, 'admin_dashboard/register_student.html')

def gen(camera):
    while True:
        ret, frame = camera.read()
        frame = cv2.flip(frame, 1)
        ret, jpeg = cv2.imencode('.jpg', frame)
        yield(b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

@gzip.gzip_page
def attached_cam(request): 
    return StreamingHttpResponse(gen(cv2.VideoCapture(0)),content_type="multipart/x-mixed-replace;boundary=frame")

def ip_cam(request):
    pass