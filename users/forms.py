from django import forms
from .models import UserProfile, AccessCode

class UserRegistrationForm(forms.ModelForm):
    access_code = forms.CharField(max_length=7, required=True)
    referral_code = forms.CharField(max_length=7, required=False)

    class Meta:
        model = UserProfile
        fields = ['name', 'phone', 'email', 'account_number', 'account_name', 'bank_name', 'access_code', 'referral_code']

    def clean_access_code(self):
        code = self.cleaned_data.get('access_code')
        if not AccessCode.objects.filter(code=code, is_used=False).exists():
            raise forms.ValidationError('Invalid or already used access code.')
        return code
