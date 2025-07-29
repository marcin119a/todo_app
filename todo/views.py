from django.shortcuts import render, redirect, get_object_or_404
from .models import Task, Project, Tag
from django.contrib.auth import login
from .forms import UserRegistrationForm, UserLoginForm, ProjectForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta

# Task list
@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    projects = Project.objects.filter(user=request.user)
    tags = Tag.objects.all()

    project_id = request.GET.get('project')
    tag_id = request.GET.get('tag')
    due_date = request.GET.get('due_date')

    if project_id:
        tasks = tasks.filter(project_id=project_id)
    if tag_id:
        tasks = tasks.filter(tags__id=tag_id)
    if due_date:
        tasks = tasks.filter(due_date=due_date)

    return render(request, 'todo/task/task_list.html', {
        'tasks': tasks,
        'projects': projects,
        'tags': tags,
        'selected_project': project_id,
        'selected_tag': tag_id,
        'selected_due_date': due_date,
    })

# Add task
@login_required
def add_task(request):
    projects = Project.objects.filter(user=request.user)
    if request.method == 'POST':
        title = request.POST.get('title')
        project_id = request.POST.get('project')
        if title:
            Task.objects.create(title=title, user=request.user, project_id=project_id)
            messages.success(request, 'Zadanie zostało dodane!')
        return redirect('task_list')
    return render(request, 'todo/task/add_task.html', {'projects': projects})

# Complete task
@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.completed = True
    task.save()
    return redirect('task_list')

@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    return render(request, 'todo/task/task_detail.html', {'task': task})


@login_required
def add_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            messages.success(request, 'Projekt został dodany!')
            return redirect('task_list')
    else:
        form = ProjectForm()
    return render(request, 'todo/user/add_project.html', {'form': form})


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
    return render(request, 'todo/user/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            from django.contrib.auth.models import User
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
    return render(request, 'todo/user/login.html', {'form': form})


def logout_view(request):
    logout(request)
    from django.shortcuts import redirect
    return redirect('login')


@login_required
def account_summary(request):
    projects = Project.objects.filter(user=request.user)
    tasks = Task.objects.filter(user=request.user)
    now = timezone.now().date()

    completed = tasks.filter(completed=True).count()
    overdue = tasks.filter(completed=False, due_date__lt=now).count()
    upcoming = tasks.filter(completed=False, due_date__gte=now, due_date__lte=now + timedelta(days=3)).count()

    return render(request, 'todo/user/account_summary.html', {
        'projects': projects,
        'completed': completed,
        'overdue': overdue,
        'upcoming': upcoming,
        'total': tasks.count(),
    })