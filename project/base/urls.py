from django.urls import path
from base import views

urlpatterns = [
    path('dashboard/', views.admin_dashboard, name="admin-dashboard"),
    path('register_student/', views.register_student, name='register-student'),
    path('attached_cam', views.attached_cam, name='attached-cam'),
    path('ip_cam/<ip>/', views.ip_cam, name='ip-cam'),
]
