from django.shortcuts import render
from django.http.response import StreamingHttpResponse, HttpResponse
from django.views.decorators import gzip

from account.models import Student
from school.models import *

import cv2
import os
import numpy as np
from PIL import Image
import json
import base64
import io
import re
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

def register_students(request):
    classes = Class.objects.all()
    context = {
        'title': "Register Students",
        'classes': classes,
    }

    if request.method == "POST":
        

    return render(request, 'admin_dashboard/register_students.html', context=context)

def gen(camera, face=False):
    while True:
        ret, frame = camera.read()
        frame = cv2.flip(frame, 1)
        ret, jpeg = cv2.imencode('.jpg', frame)
        yield(b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

@gzip.gzip_page
def attached_cam(request): 
    if request.method == "POST":
        imagestr = request.POST["imageData"]
        imagestr = re.sub('^data:image/.+;base64,', '', imagestr)
        (w,h) = request.POST["width"], request.POST["height"]
        imgdata = base64.b64decode(str(imagestr))
        image = Image.open(io.BytesIO(imgdata))
        image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)

        models_dir = os.path.join(module_dir, "models")
        prototxtPath = os.path.join(models_dir, "Resnet_SSD_deploy.prototxt")
        weightsPath = os.path.join(models_dir, "Res10_300x300_SSD_iter_140000.caffemodel")
        faceNet = cv2.dnn.readNetFromCaffe(
        prototxtPath, weightsPath)
        (h, w) = image.shape[:2]
        blob = cv2.dnn.blobFromImage(image, 1.0, (224, 224),
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
                
                image = image[startY:endY, startX:endX]

        ret, jpeg = cv2.imencode('.jpg', image)
        return HttpResponse(json.dumps({"image": base64.b64encode(jpeg).decode()}), content_type='application/json')
 
    models_dir = os.path.join(module_dir, "models")
    return StreamingHttpResponse(gen(cv2.VideoCapture(0)),content_type="multipart/x-mixed-replace;boundary=frame")

def ip_cam(request, ip):
    pass