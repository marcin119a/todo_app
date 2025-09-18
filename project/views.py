from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
from .forms import ProjectForm
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import get_user_model
from .models import Project, ProjectComment
from todo.models import Task
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods


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

@login_required
def project_detail(request, project_id):
    """View for displaying project details with comments"""
    project = get_object_or_404(Project, id=project_id)
    
    # Check if user has access to this project
    if project.user != request.user and request.user not in project.members.all():
        messages.error(request, 'Nie masz uprawnień do przeglądania tego projektu.')
        return redirect('project_list')
    
    # Get comments for this project
    comments = project.comments.all()
    
    context = {
        'project': project,
        'comments': comments,
    }
    return render(request, 'project/project_detail.html', context)


@login_required
@require_http_methods(["POST"])
def add_project_comment(request, project_id):
    """API view for adding comments to projects"""
    try:
        # Parse JSON data
        data = json.loads(request.body)
        content = data.get('content', '').strip()
        
        # Validate content
        if not content:
            return JsonResponse({
                'success': False,
                'error': 'Treść komentarza nie może być pusta.'
            }, status=400)
        
        # Get project and check permissions
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return HttpResponse(
                json.dumps({
                    'success': False,
                    'error': 'Projekt nie został znaleziony.'
                }),
                content_type='application/json',
                status=404
            )
            
        if project.user != request.user and request.user not in project.members.all():
            return JsonResponse({
                'success': False,
                'error': 'Nie masz uprawnień do dodawania komentarzy do tego projektu.'
            }, status=403)
        
        # Create comment
        comment = ProjectComment.objects.create(
            user=request.user,
            project=project,
            content=content,
            author=request.user.username
        )
        
        # Return success response with comment data
        return JsonResponse({
            'success': True,
            'comment': {
                'id': comment.id,
                'content': comment.content,
                'author': comment.author,
                'created_at': comment.created_at.strftime('%d.%m.%Y %H:%M'),
                'user_id': comment.user.id
            }
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Nieprawidłowy format JSON.'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': 'Wystąpił błąd podczas dodawania komentarza.'
        }, status=500)