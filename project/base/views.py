from django.shortcuts import render
from account.models import Student
from school.models import *

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
