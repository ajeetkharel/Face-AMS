from django.urls import path
from school import views

urlpatterns = [
    path('view-students/<id>/', views.view_students, name="view-students"),
    path('view-attendance/<id>/', views.view_attendance, name="view-attendance"),
]
