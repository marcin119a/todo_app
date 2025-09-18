from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import PasswordChangeForm
from .models import Task, Tag

class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            existing_classes = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = (existing_classes + ' form-control').strip()

class UserRegistrationForm(BootstrapFormMixin, forms.ModelForm):
    password = forms.CharField(label='Hasło', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Powtórz hasło', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Użytkownik z tym adresem e-mail już istnieje.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise ValidationError('Hasła muszą być identyczne.')
        if password:
            validate_password(password)
        return cleaned_data

class UserLoginForm(BootstrapFormMixin, forms.Form):
    email = forms.EmailField(label='E-mail', widget=forms.EmailInput())
    password = forms.CharField(label='Password', widget=forms.PasswordInput())


class TaskForm(BootstrapFormMixin, forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Tagi'
    )

    class Meta:
        model = Task
        fields = ['title', 'project', 'due_date', 'priority', 'tags']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }
