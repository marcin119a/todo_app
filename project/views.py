from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
from .forms import ProjectForm
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import get_user_model
from .models import Project
from todo.models import Task
from django.shortcuts import get_object_or_404

User = get_user_model()

# Create your views here.


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
    return render(request, 'project/add_project.html', {'form': form})


class AddMemberAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk, format=None):
        project = Project.objects.get(pk=pk)
        if project.user != request.user and request.user not in project.members.all():
            return Response({'error': 'Brak uprawnień do edycji tego projektu.'}, status=status.HTTP_403_FORBIDDEN)
        username = request.data.get('username')
        try:
            user_to_add = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': 'Nie znaleziono użytkownika.'}, status=status.HTTP_404_NOT_FOUND)
        project.members.add(user_to_add)
        return Response({'success': True, 'added_user': user_to_add.username})

@login_required
def project_list(request):
    projects = Project.objects.filter(user=request.user)
    return render(request, 'project/project_list.html', {'projects': projects})

@login_required
def edit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            project = form.save()
            # Zaktualizuj członków projektu
            project.members.set(form.cleaned_data['members'])
            messages.success(request, 'Projekt został zaktualizowany!')
            return redirect('task_list')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'project/edit_project.html', {'form': form, 'project': project})


@login_required
def calendar_view(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'project/calendar.html', {'tasks': tasks})