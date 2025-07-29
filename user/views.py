from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from todo.forms import UserRegistrationForm, UserLoginForm
from todo.models import Project, Task
from django.utils import timezone
from datetime import timedelta


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('task_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'user/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(email=email)
                user = authenticate(request, username=user.username, password=password)
            except User.DoesNotExist:
                user = None
            if user is not None:
                login(request, user)
                return redirect('task_list')
            else:
                messages.error(request, 'Nieprawidłowy e-mail lub hasło.')
    else:
        form = UserLoginForm()
    return render(request, 'user/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def account_summary(request):
    projects = Project.objects.filter(user=request.user)
    tasks = Task.objects.filter(user=request.user)
    now = timezone.now().date()

    completed = tasks.filter(completed=True).count()
    overdue = tasks.filter(completed=False, due_date__lt=now).count()
    upcoming = tasks.filter(completed=False, due_date__gte=now, due_date__lte=now + timedelta(days=3)).count()

    return render(request, 'user/account_summary.html', {
        'projects': projects,
        'completed': completed,
        'overdue': overdue,
        'upcoming': upcoming,
        'total': tasks.count(),
    })
