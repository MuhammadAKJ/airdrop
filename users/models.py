import random
import string
from django.db import models


def generate_access_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))


class AccessCode(models.Model):
    code = models.CharField(max_length=7, unique=True)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.code}'

class UserProfile(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15, unique=True, primary_key=True)
    email = models.EmailField(unique=True)
    account_number = models.CharField(max_length=20)
    account_name = models.CharField(max_length=255)
    bank_name = models.CharField(max_length=255)
    referral_code = models.CharField(max_length=7, blank=True, null=True)
    referral_points = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.name}'
        

class DailyTask(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    coin_clicks = models.IntegerField(default=0)
    points = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.name} - {self.coin_clicks} clicks'


class WithdrawalRequest(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    points_to_withdraw = models.IntegerField()
    is_approved = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.name} - {self.points_to_withdraw} points'


class MonthlyTask(models.Model):
    title = models.CharField(max_length=255)
    task_url = models.URLField()
    points = models.IntegerField(default=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title}'


class UserMonthlyTask(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    task = models.ForeignKey(MonthlyTask, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)



"""
class MonthlyTask(models.Model):
    title = models.CharField(max_length=255)
    link = models.URLField()
    points = models.IntegerField(default=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class CompletedTask(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    task = models.ForeignKey(MonthlyTask, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.name} - {self.task.title}'
"""