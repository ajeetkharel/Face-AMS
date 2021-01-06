from django.urls import path
from base import views

urlpatterns = [
    path('dashboard/', views.admin_dashboard, name="admin-dashboard")
]
