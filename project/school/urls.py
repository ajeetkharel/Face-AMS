from django.urls import path
from school import views

urlpatterns = [
    path('view-students/<id>/', views.view_students, name="view-students"),
    path('view-attendance/<id>/', views.view_attendance, name="view-attendance"),
    path('manage-feedbacks/', views.manage_feedbacks, name="manage-feedbacks"),
    
    path('attendance/', views.student_attendance, name='student-attendance'),
    path('student-attendance/<pk>/', views.admin_student_attendance, name='admin-student-attendance'),
    path('profile/', views.student_profile, name='student-profile'),
]