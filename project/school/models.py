from django.db import models

class Class(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Routine(models.Model):
    time = models.TimeField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Attendance(models.Model):
    date = models.DateTimeField(auto_now=False, auto_now_add=True)
    
    def __str__(self):
        return self.name