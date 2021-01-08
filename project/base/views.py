from django.shortcuts import render
from django.http.response import StreamingHttpResponse
from django.views.decorators import gzip

from account.models import Student
from school.models import *

import cv2
import os
import numpy as np
module_dir = os.path.dirname(__file__)

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
    models_dir = os.path.join(module_dir)
    prototxtPath = os.path.join(models_dir, "models", "Resnet_SSD_deploy.prototxt")
    weightsPath = os.path.join(models_dir, "models", "Res10_300x300_SSD_iter_140000.caffemodel")
    faceNet = cv2.dnn.readNetFromCaffe(
        prototxtPath, weightsPath)
    while True:
        ret, frame = camera.read()
        frame = cv2.flip(frame, 1)
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(frame, 1.0, (224, 224),
            (104.0, 177.0, 123.0))

        faceNet.setInput(blob)
        detections = faceNet.forward()

        faces = []
        locs = []
        preds = []

        for i in range(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]

            if confidence > 0.5:
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                (startX, startY) = (max(0, startX), max(0, startY))
                (endX, endY) = (min(w - 1, endX), min(h - 1, endY))

                cv2.rectangle(frame, (startX, startY), (endX, endY), (255,0,0), 2)
        ret, jpeg = cv2.imencode('.jpg', frame)
        yield(b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

@gzip.gzip_page
def attached_cam(request): 
    return StreamingHttpResponse(gen(cv2.VideoCapture(0)),content_type="multipart/x-mixed-replace;boundary=frame")

def ip_cam(request, ip):
    pass