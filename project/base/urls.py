from django.urls import path
from base import views

urlpatterns = [
    path('dashboard/', views.admin_dashboard, name="admin-dashboard"),
    path('register_students/', views.register_students, name='register-students'),
    path('attached_cam', views.attached_cam, name='attached-cam'),
    path('ip_cam/<ip>/', views.ip_cam, name='ip-cam'),
]
