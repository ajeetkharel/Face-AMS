from django.contrib import admin
from school.models import *


class StudentAdmin(admin.ModelAdmin):
    readonly_fields = ('student_id', )

admin.site.register(Student, StudentAdmin)
admin.site.register(Class)
admin.site.register(Routine)
admin.site.register(Subject)
admin.site.register(Attendance)