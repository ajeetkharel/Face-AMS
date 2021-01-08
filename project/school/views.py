from django.shortcuts import render
from school.models import *
from account.models import Student


def view_students(request, id):
    cls = Class.objects.get(id=id)
    students = Student.objects.filter(study_class=cls)

    context = {
        'class': cls,
        'students':students,
    }

    return render(request, "admin_dashboard/manage_students.html", context=context)