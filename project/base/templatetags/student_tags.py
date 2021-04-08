from django import template
from school.models import Attendance, Student
from datetime import datetime

register = template.Library()

@register.filter
def get_present(student):
    try:
        attendances = Attendance.objects.filter(student=student.pk, date__year = datetime.now().year)
        return attendances.count()
    except Attendance.DoesNotExist:
        return 0


@register.filter
def get_absent(student):
    try:
        attendances = Attendance.objects.filter(student=student.pk, date__year = datetime.now().year)
        return 220 - attendances.count()
    except Attendance.DoesNotExist:
        return 0
