from django.contrib import admin
from .models import AccessCode
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.urls import path
from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from .models import generate_access_code
from django.contrib import messages
from .models import MonthlyTask


@admin.register(AccessCode)
class AccessCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'is_used', 'created_at')

    # Add custom action button to generate access codes
    change_list_template = "admin/accesscode_changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('generate/', self.generate_access_code_view, name='generate_access_code'),
        ]
        return custom_urls + urls

    def generate_access_code_view(self, request):
        # Generate new access code
        new_code = generate_access_code()
        AccessCode.objects.create(code=new_code)

        # Redirect back to admin page
        self.message_user(request, f"Access code '{new_code}' generated successfully.")
        return HttpResponseRedirect("../")


@admin.register(MonthlyTask)
class MonthlyTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'task_url', 'points', 'created_at')


