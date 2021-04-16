from django.shortcuts import render
from school.models import *
import datetime

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

    if request.is_ajax():
        startdate = datetime.datetime.strptime(request.GET["startdate"], "%Y-%m-%d")
        enddate = datetime.datetime.strptime(request.GET["enddate"], "%Y-%m-%d")

        attendances = attendances.filter(date__gte=startdate, date__lte=enddate)
        print(attendances)
        context['attendances'] = attendances

    return render(request, "admin_dashboard/manage_attendance.html", context=context)
    
def manage_feedbacks(request):
    return render(request, "admin_dashboard/manage_feedbacks.html")


def student_attendance(request):
    student = Student.objects.get(user=request.user)
    attendances = Attendance.objects.filter(student=student)
    context = {
        'title': 'Student Attendance',
        'attendances': attendances,
        'student': student
    }

    return render(request, 'student_dashboard/student_attendance.html', context=context)

def admin_student_attendance(request, pk):
    student = Student.objects.get(pk=pk)
    attendances = Attendance.objects.filter(student=student)
    context = {
        'title': 'Student Attendance',
        'attendances': attendances,
        'student': student,
        'classes': Class.objects.all(),
    }

    return render(request, 'admin_dashboard/student_attendance.html', context=context)


def student_profile(request):
    student = Student.objects.get(user=request.user)
    context = {
        'title': 'Student Profile',
        'student': student,
    }
    if request.method == "POST":
        user = User.objects.get(id=request.user.pk)
        profile_image = request.FILES["profile_image"]
        user.profile_image = profile_image
        user.save()

    return render(request, "student_dashboard/student_profile.html", context=context)


