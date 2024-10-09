from datetime import datetime

from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .forms import UserRegistrationForm
from .models import AccessCode, UserProfile
from .models import DailyTask, WithdrawalRequest
from .models import MonthlyTask, UserMonthlyTask


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Save the user profile
            user = form.save(commit=False)
            access_code = form.cleaned_data['access_code']
            referral_code = form.cleaned_data.get('referral_code', None)

            # Mark the access code as used
            AccessCode.objects.filter(code=access_code).update(is_used=True)

            # Handle referral system
            if referral_code:
                referrer = UserProfile.objects.filter(referral_code=referral_code).first()
                if referrer:
                    referrer.referral_points += 1
                    referrer.save()

            # Save the user profile
            user.save()
            return redirect('login')  # Redirect to login after registration
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})


def leaderboard(request):
    users = UserProfile.objects.order_by('-referral_points')[:10]  # Top 10 users by referral points
    return render(request, 'users/leaderboard.html', {'users': users})

class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    authentication_form = AuthenticationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('dashboard')  # Redirect to dashboard or homepage after login


@login_required
def dashboard(request):
    return render(request, 'users/dashboard.html')


def daily_task(request):
    user = request.user.userprofile  # Assuming the user is authenticated
    daily_task, created = DailyTask.objects.get_or_create(user=user)

    if request.method == 'POST':
        if daily_task.coin_clicks < 200:
            daily_task.coin_clicks += 1
            daily_task.save()

        if daily_task.coin_clicks == 200:
            daily_task.points += 10  # Reward for 200 clicks
            daily_task.coin_clicks = 0  # Reset for the next day
            daily_task.save()

    return render(request, 'users/daily_task.html', {'daily_task': daily_task})


def request_withdrawal(request):
    user = request.user.userprofile
    current_day = datetime.now().strftime('%A')

    # Check if it's Saturday
    if current_day != 'Saturday':
        return render(request, 'users/withdraw.html', {'error': 'Withdrawals are only allowed on Saturdays.'})

    # Check referral points and daily task points
    if user.referral_points >= 10:
        points_to_withdraw = int(user.referral_points * 0.7)  # 70% of referral points
        if request.method == 'POST':
            # Create a withdrawal request
            WithdrawalRequest.objects.create(user=user, points_to_withdraw=points_to_withdraw)
            user.referral_points -= points_to_withdraw
            user.save()
            return redirect('withdrawal_success')

    if DailyTask.objects.get(user=user).points >= 20000000:
        if request.method == 'POST':
            # Create a withdrawal request for daily task points
            WithdrawalRequest.objects.create(user=user, points_to_withdraw=DailyTask.objects.get(user=user).points)
            DailyTask.objects.get(user=user).points = 0  # Reset daily task points after withdrawal
            DailyTask.objects.get(user=user).save()
            return redirect('withdrawal_success')

    return render(request, 'users/withdraw.html', {'points_to_withdraw': points_to_withdraw})


@staff_member_required
def manage_payments(request):
    pending_requests = WithdrawalRequest.objects.filter(is_approved=True, is_paid=False)

    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        withdrawal_request = WithdrawalRequest.objects.get(id=request_id)
        withdrawal_request.is_paid = True
        withdrawal_request.save()

    return render(request, 'users/manage_payments.html', {'pending_requests': pending_requests})



def monthly_tasks(request):
    user = request.user.userprofile
    tasks = MonthlyTask.objects.all()

    for task in tasks:
        user_task, created = UserMonthlyTask.objects.get_or_create(user=user, task=task)

    return render(request, 'users/monthly_tasks.html', {'tasks': tasks, 'user': user})

def complete_task(request, task_id):
    task = MonthlyTask.objects.get(id=task_id)
    user = request.user.userprofile
    user_task = UserMonthlyTask.objects.get(user=user, task=task)

    if not user_task.is_completed:
        user_task.is_completed = True
        user_task.completed_at = timezone.now()
        user_task.save()

        # Add points to the user
        user.referral_points += task.points
        user.save()

    return redirect('monthly_tasks')
