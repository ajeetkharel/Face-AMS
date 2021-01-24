from django.shortcuts import render
from school.models import *


def view_students(request, id):
    cls = Class.objects.get(id=id)
    students = Student.objects.filter(study_class=cls)
    classes = Class.objects.all()

    context = {
        'title': "Students - "+cls.name,
        'class': cls,
        'students':students,
        'classes': classes,
    }

    return render(request, "admin_dashboard/manage_students.html", context=context)

def view_attendance(request, id):
    cls = Class.objects.get(id=id)
    students = Student.objects.filter(study_class=cls)
    classes = Class.objects.all()
    attendances = Attendance.objects.filter(student__in=students)

    context = {
        'class': cls,
        'students':students,
        'classes': classes,
        'attendances': attendances,
    }

    return render(request, "admin_dashboard/manage_attendance.html", context=context)
    