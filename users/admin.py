from django.contrib import admin
from .models import AccessCode
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied

@admin.register(AccessCode)
class AccessCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'is_used', 'created_at')
    actions = ['generate_access_codes']

    def generate_access_codes(self, request, queryset):
        if not request.user.is_superuser:
            raise PermissionDenied
        for _ in range(10):  # Generates 10 codes at once
            code = AccessCode.generate_code()
            AccessCode.objects.create(code=code)
        self.message_user(request, "Access codes generated successfully.")
    generate_access_codes.short_description = "Generate new access codes"


    