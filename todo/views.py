from django.shortcuts import render, redirect, get_object_or_404
from .models import Task, Tag
from project.models import Project
from django.contrib.auth import login, logout
from .forms import UserRegistrationForm, UserLoginForm, TaskForm
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
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User

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


class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'todo/task/edit_task.html'
    pk_url_kwarg = 'task_id'
    success_url = reverse_lazy('task_list')

    def get_queryset(self):
        # Only tasks belonging to the current user
        return Task.objects.filter(user=self.request.user)

    def get_success_url(self):
        # Redirect to task detail page after successful update
        return reverse_lazy('task_detail', kwargs={'task_id': self.object.id})

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Zadanie zostało zaktualizowane!')
        return response


@require_http_methods(["GET", "POST"])
def api_tags(request):
    """API endpoint to get all available tags and create new ones"""
    if request.method == "GET":
        tags = Tag.objects.all().values_list('name', flat=True)
        return JsonResponse({'tags': list(tags)})
    
    elif request.method == "POST":
        try:
            import json
            data = json.loads(request.body)
            tag_name = data.get('name', '').strip()
            
            if not tag_name:
                return JsonResponse({'error': 'Nazwa tagu jest wymagana'}, status=400)
            
            # Check if tag already exists
            if Tag.objects.filter(name=tag_name).exists():
                return JsonResponse({'error': 'Tag już istnieje'}, status=400)
            
            # Create new tag
            new_tag = Tag.objects.create(name=tag_name)
            return JsonResponse({
                'success': True,
                'tag': {
                    'id': new_tag.id,
                    'name': new_tag.name
                }
            })
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Nieprawidłowy format JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
