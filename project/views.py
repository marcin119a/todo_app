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
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy

User = get_user_model()



class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'project/add_project.html'
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        self.object.members.set(form.cleaned_data['members'])
        messages.success(self.request, 'Projekt został dodany!')
        return response



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

class ProjectUpdateView(UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'project/edit_project.html'
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



@login_required
def calendar_view(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'project/calendar.html', {'tasks': tasks})