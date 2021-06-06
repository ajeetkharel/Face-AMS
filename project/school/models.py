from django.db import models
from account.models import User
import datetime

class Class(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Student(models.Model):
    student_id = models.AutoField(primary_key=True, auto_created=True, default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact = models.CharField(max_length=255, default='', blank=True)
    address = models.CharField(max_length=255, default='', blank=True)
    face_encoding = models.BinaryField(blank=True)
    study_class = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.email

class Subject(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Routine(models.Model):
    start_time = models.TimeField(auto_now=False, auto_now_add=False, default=datetime.datetime.now().time())
    end_time = models.TimeField(auto_now=False, auto_now_add=False, default=datetime.datetime.now().time())
    _class = models.ForeignKey(Class, on_delete=models.CASCADE, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self._class} {self.subject}"


class Attendance(models.Model):
    date = models.DateTimeField()
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    routine = models.ForeignKey(Routine, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=1, default="P")
    def __str__(self):
        return f"{self.date}-{self.student.student_id}"


class Feedback(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    subject = models.CharField(max_length=255, default='')
    message = models.TextField()

    def __str__(self):
        return f"Feedback from {self.student.user.full_name} - {self.subject}"