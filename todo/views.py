from django.shortcuts import render, redirect, get_object_or_404
from .models import Task, Tag
from project.models import Project
from django.contrib.auth import login, logout
from .forms import UserRegistrationForm, UserLoginForm
from project.forms import ProjectForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render
from comments.models import Comment
from django.views.generic import UpdateView, DeleteView
from django.urls import reverse_lazy

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
    today = timezone.now().date()
    if request.method == 'POST':
        title = request.POST.get('title')
        project_id = request.POST.get('project')
        due_date = request.POST.get('due_date')
        if title:
            Task.objects.create(title=title, user=request.user, project_id=project_id, due_date=due_date)
            messages.success(request, 'Zadanie zostało dodane!')
        return redirect('task_list')
    return render(request, 'todo/task/add_task.html', {'projects': projects, 'today': today})

# Complete task
@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        task.completed = 'completed' in request.POST
        task.save()
    return redirect('task_list')

@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    comments = Comment.objects.filter(task=task).order_by('created_at')
    return render(request, 'todo/task/task_detail.html', {'task': task, 'comments': comments})


class ProjectUpdateView(UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'todo/project/edit_project.html'
    pk_url_kwarg = 'project_id'
    success_url = reverse_lazy('task_list')

    def get_queryset(self):
        # Tylko projekty użytkownika
        return Project.objects.filter(user=self.request.user)

    def form_valid(self, form):
        response = super().form_valid(form)
        # Zaktualizuj członków projektu
        self.object.members.set(form.cleaned_data['members'])
        messages.success(self.request, 'Projekt został zaktualizowany!')
        return response


class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'todo/task/task_confirm_delete.html'
    success_url = reverse_lazy('task_list')

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


