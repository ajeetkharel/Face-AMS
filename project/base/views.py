from django.shortcuts import render, redirect
from django.http.response import StreamingHttpResponse, HttpResponse
from django.views.decorators import gzip
from django.core.files.base import ContentFile
from django.contrib.auth.base_user import BaseUserManager
from django.core.mail import send_mail
from django.conf import settings

from account.models import User
from school.models import *

import cv2
import os
import numpy as np
from PIL import Image
import json
import base64
import io
import pickle
import re
import face_recognition
from datetime import datetime, timedelta
from collections import OrderedDict


module_dir = os.path.dirname(__file__)


from chartjs.views.lines import BaseLineChartView


def dashboard(request):
    if request.user.is_staff:
        classes = Class.objects.all().order_by('-name')
        context = {
            'title': "Admin Dashboard",
            'classes': classes,
        }
        return render(request, "admin_dashboard/index.html", context=context)

    else:
        return redirect('student-dashboard')


def student_dashboard(request):
    if request.user.is_authenticated:
        student = Student.objects.get(user=request.user)
        context = {
            'title': "Student Dashboard",
            'student': student,
        }
        return render(request, "student_dashboard/index.html", context=context)
    else:
        return redirect('user-login')

def register_students(request):
    classes = Class.objects.all().order_by('-name')
    context = {
        'title': "Register Students",
        'classes': classes,
    }

    if request.method == "POST":
        message = {"error": False}
        if Student.objects.filter(student_id = int(request.POST["student_id"])).exists():
            message["id_error"] = "ID already exists"
            message["error"] = True
        
        if User.objects.filter(email=request.POST["email"]).exists():
            message["email_error"] = "Email already exists"
            message['error'] = True

        if not message["error"]:
            profile_image = request.POST["student_face"]
            user = User.objects.create(full_name=request.POST["full_name"], email=request.POST["email"])
            password = BaseUserManager().make_random_password()
            user.set_password(password)
            user.save()

            student = Student.objects.create(student_id=int(request.POST["student_id"]), user=user, contact=request.POST["contact"],
             address=request.POST["address"], study_class=Class.objects.get(pk=int(request.POST["class"])))
            image_data = base64.b64decode(profile_image.replace("data:image/jpeg;base64,", ""))
            image = Image.open(io.BytesIO(image_data))


            
            img_io = io.BytesIO()
            image.save(img_io, format='JPEG', quality=100)
            # img_content = ContentFile(img_io.getvalue(), f'{request.POST["student_id"]}_face.jpg')

            encoding = face_recognition.face_encodings(np.array(image))
            print(encoding)
            np_bytes = pickle.dumps(encoding)
            np_base64 = base64.b64encode(np_bytes)
            student.face_encoding = np_base64

            #https://stackoverflow.com/questions/46699238/how-to-make-a-numpy-array-field-in-django
            
            # student.profile_image = img_content
            student.save()

            message["student_id"] = student.student_id
            message["email"] = student.user.email
            message["password"] = password

            send_mail('Face AMS Account Details',
            f"Please don't share this to anyone \n \
    Email: {request.POST['email']} \n \
    Password: {password} ", settings.EMAIL_HOST_USER, [request.POST["email"]])

            # return render(request, 'admin_dashboard/register_students.html', context=context)
        return HttpResponse(json.dumps(message), content_type='application/json')
        
    return render(request, 'admin_dashboard/register_students.html', context=context)

def gen(camera, face=False):
    while True:
        ret, frame = camera.read()
        frame = cv2.flip(frame, 1)
        ret, jpeg = cv2.imencode('.jpg', frame)
        yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

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
        for i in range(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.5:
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                (startX, startY) = (max(0, startX), max(0, startY))
                (endX, endY) = (min(w - 1, endX), min(h - 1, endY))
                image = image[startY:endY, startX:endX]
        ret, jpeg = cv2.imencode('.jpg', image)
        encoded = base64.b64encode(jpeg)
        decoded = encoded.decode()

        jsondata = json.dumps({"image": decoded})
        return HttpResponse(jsondata, content_type='application/json')
 
    models_dir = os.path.join(module_dir, "models")
    return StreamingHttpResponse(gen(cv2.VideoCapture(0))
                    ,content_type="multipart/x-mixed-replace;boundary=frame")

def ip_cam(request, ip):
    pass


class LineChartJSONView(BaseLineChartView):
    current_date = datetime.now()

    dates = [f"{current_date.year}-01-01", f"{current_date.date().strftime('%Y-%m-%d')}"]
    start, end = [datetime.strptime(_, "%Y-%m-%d") for _ in dates]

    def get_labels(self):
        listt = OrderedDict(((self.start + timedelta(_)).strftime(r"%B"), None) for _ in range((self.end - self.start).days)).keys()
        return list(listt)

    def get_providers(self):
        """Return names of datasets."""
        return ["Present", "Absent"]

    def get_data(self):
        """Return 3 datasets to plot."""
        months = OrderedDict(((self.start + timedelta(_)).strftime(r"%m"), None) for _ in range((self.end - self.start).days)).keys()

        data = [[], []]
        for month in months:
            attendances = Attendance.objects.filter(date__year=self.current_date.year, date__month=month)

            data[0].append(len(attendances.filter(status="P")))
            data[1].append(len(attendances.filter(status="A")))
        return data
