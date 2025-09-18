from django import forms
from django.contrib.auth import get_user_model
from todo.forms import BootstrapFormMixin

User = get_user_model()


class ProjectForm(BootstrapFormMixin, forms.ModelForm):
    members = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control', 'id': 'id_members'}),
        label='Participants',
        help_text='Chose users who should be part of the project.'
    )
    class Meta:
        model = User._meta.get_field('projects').related_model
        fields = ['name', 'description', 'members']
        widgets = {
            'name': forms.TextInput(),
            'description': forms.Textarea({'rows': 3}),
        }

