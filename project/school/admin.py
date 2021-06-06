from django.contrib import admin
from school.models import *


class StudentAdmin(admin.ModelAdmin):
    readonly_fields = ('student_id', )


class RoutineAdmin(admin.ModelAdmin):
    model = Routine
    list_display = ('subject','start_time', 'end_time', '_class')


class SubjectAdmin(admin.ModelAdmin):
    model = Subject
    list_display = ('name',)

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'date')

admin.site.register(Student, StudentAdmin)
admin.site.register(Class)
admin.site.register(Routine, RoutineAdmin)


admin.site.register(Subject, SubjectAdmin)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(Feedback)