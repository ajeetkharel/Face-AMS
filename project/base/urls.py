from django.urls import path
from base import views
from django.views.generic import TemplateView

urlpatterns = [
    path('dashboard/', views.dashboard, name="dashboard"),
    path('register_students/', views.register_students, name='register-students'),
    path('attached_cam', views.attached_cam, name='attached-cam'),
    path('ip_cam/<ip>/', views.ip_cam, name='ip-cam'),


    path("student-dashboard/", views.student_dashboard, name='student-dashboard'),

    path('chart', TemplateView.as_view(template_name='admin_dashboard/index.html'), name='line_chart'),
    path('chartJSON', views.LineChartJSONView.as_view(), name='line_chart_json'),
]
