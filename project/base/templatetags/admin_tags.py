from django import template
from datetime import datetime
from school.models import Attendance

register = template.Library()

@register.filter(name='todate')
def convert_str_date(value):
    return datetime.strptime(value, '%Y-%m-%d').date()

@register.filter
def get_present(a):
    try:
        attendances = Attendance.objects.filter(date__year = datetime.now().year, status="P")
        return attendances.count()
    except Attendance.DoesNotExist:
        return 0


@register.filter
def get_absent(a):
    try:
        attendances = Attendance.objects.filter(date__year = datetime.now().year, status="A")
        return attendances.count()
    except Attendance.DoesNotExist:
        return 0

