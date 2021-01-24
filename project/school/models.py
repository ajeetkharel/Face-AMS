from django.db import models
from account.models import User


class Class(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Student(models.Model):
    student_id = models.AutoField(primary_key=True, auto_created=True, default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact = models.CharField(max_length=255, default='', blank=True)
    address = models.CharField(max_length=255, default='', blank=True)
    face_image = models.ImageField(upload_to="face_images/", default="face_images/default.jpg")
    face_encoding = models.BinaryField(blank=True)
    study_class = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.email

class Routine(models.Model):
    time = models.TimeField(auto_now=False, auto_now_add=False)
    _class = models.ForeignKey(Class, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.time}"

class Subject(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Attendance(models.Model):
    STATUS_CHOICES = (
        ("P", "Present"),
        ("A", "Absent")
    )
    date = models.DateTimeField(auto_now=False, auto_now_add=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    routine = models.ForeignKey(Routine, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=7, default="P", choices=STATUS_CHOICES)
    def __str__(self):
        return f"{self.date}-{self.student.student_id}"
