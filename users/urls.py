"""
from django.urls import path
from .views import register

urlpatterns = [
    path('register/', register, name='register'),
]
"""
from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import register, leaderboard, daily_task
from .views import request_withdrawal, manage_payments
from .views import monthly_tasks, complete_task, dashboard
from .views import CustomLoginView


urlpatterns = [
    path('register/', register, name='register'),
    path('leaderboard/', leaderboard, name='leaderboard'),
    path('daily-task/', daily_task, name='daily_task'),
    path('withdraw/', request_withdrawal, name='withdraw'),
    path('admin/manage-payments/', manage_payments, name='manage_payments'),
    path('monthly-tasks/', monthly_tasks, name='monthly_tasks'),
    path('complete-task/<int:task_id>/', complete_task, name='complete_task'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
]