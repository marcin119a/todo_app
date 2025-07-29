from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'email']

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar'] 