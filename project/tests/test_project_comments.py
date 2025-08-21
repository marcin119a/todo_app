import pytest
import json
from django.contrib.auth import get_user_model
from project.models import Project
from todo.models import Task

User = get_user_model()


@pytest.mark.django_db
def test_user_can_view_project_detail_with_comments(client):
    """Test that user can view project details page with comments section"""
    user = User.objects.create_user(username='testuser', password='testpass')
    project = Project.objects.create(user=user, name='Test Project', description='Test Description')
    
    client.force_login(user)
    response = client.get(f'/project/project/{project.id}/')
    
    assert response.status_code == 200
    assert 'project' in response.context
    assert 'comments' in response.context
    assert response.context['project'] == project


@pytest.mark.django_db
def test_user_can_add_comment_to_project(client):
    """Test that logged in user can add comment to project"""
    user = User.objects.create_user(username='testuser', password='testpass')
    project = Project.objects.create(user=user, name='Test Project')
    
    client.force_login(user)
    url = f'/project/project/{project.id}/add-comment/'
    data = {
        'content': 'To jest testowy komentarz do projektu'
    }
    
    response = client.post(url, json.dumps(data), content_type='application/json')
    
    assert response.status_code == 200
    response_data = json.loads(response.content)
    assert response_data['success'] is True
    assert response_data['comment']['content'] == 'To jest testowy komentarz do projektu'
    assert response_data['comment']['author'] == user.username


@pytest.mark.django_db
def test_project_owner_can_add_comment(client):
    """Test that project owner can add comment to their project"""
    owner = User.objects.create_user(username='owner', password='testpass')
    project = Project.objects.create(user=owner, name='Owner Project')
    
    client.force_login(owner)
    url = f'/project/project/{project.id}/add-comment/'
    data = {
        'content': 'Komentarz od właściciela projektu'
    }
    
    response = client.post(url, json.dumps(data), content_type='application/json')
    
    assert response.status_code == 200
    response_data = json.loads(response.content)
    assert response_data['success'] is True


@pytest.mark.django_db
def test_project_member_can_add_comment(client):
    """Test that project member can add comment to project"""
    owner = User.objects.create_user(username='owner', password='testpass')
    member = User.objects.create_user(username='member', password='testpass')
    project = Project.objects.create(user=owner, name='Shared Project')
    project.members.add(member)
    
    client.force_login(member)
    url = f'/project/project/{project.id}/add-comment/'
    data = {
        'content': 'Komentarz od członka zespołu'
    }
    
    response = client.post(url, json.dumps(data), content_type='application/json')
    
    assert response.status_code == 200
    response_data = json.loads(response.content)
    assert response_data['success'] is True


@pytest.mark.django_db
def test_unauthorized_user_cannot_add_comment(client):
    """Test that unauthorized user cannot add comment to project"""
    owner = User.objects.create_user(username='owner', password='testpass')
    unauthorized_user = User.objects.create_user(username='unauthorized', password='testpass')
    project = Project.objects.create(user=owner, name='Private Project')
    
    client.force_login(unauthorized_user)
    url = f'/project/project/{project.id}/add-comment/'
    data = {
        'content': 'Próba dodania komentarza przez nieautoryzowanego użytkownika'
    }
    
    response = client.post(url, json.dumps(data), content_type='application/json')
    
    assert response.status_code == 403


@pytest.mark.django_db
def test_anonymous_user_cannot_add_comment(client):
    """Test that anonymous user cannot add comment to project"""
    owner = User.objects.create_user(username='owner', password='testpass')
    project = Project.objects.create(user=owner, name='Test Project')
    
    url = f'/project/project/{project.id}/add-comment/'
    data = {
        'content': 'Próba dodania komentarza przez anonimowego użytkownika'
    }
    
    response = client.post(url, json.dumps(data), content_type='application/json')
    
    assert response.status_code == 302  # Redirect to login


@pytest.mark.django_db
def test_empty_comment_is_rejected(client):
    """Test that empty comment content is rejected"""
    user = User.objects.create_user(username='testuser', password='testpass')
    project = Project.objects.create(user=user, name='Test Project')
    
    client.force_login(user)
    url = f'/project/project/{project.id}/add-comment/'
    data = {
        'content': ''
    }
    
    response = client.post(url, json.dumps(data), content_type='application/json')
    
    assert response.status_code == 400
    response_data = json.loads(response.content)
    assert 'error' in response_data


@pytest.mark.django_db
def test_whitespace_only_comment_is_rejected(client):
    """Test that comment with only whitespace is rejected"""
    user = User.objects.create_user(username='testuser', password='testpass')
    project = Project.objects.create(user=user, name='Test Project')
    
    client.force_login(user)
    url = f'/project/project/{project.id}/add-comment/'
    data = {
        'content': '   \n\t   '
    }
    
    response = client.post(url, json.dumps(data), content_type='application/json')
    
    assert response.status_code == 400
    response_data = json.loads(response.content)
    assert 'error' in response_data


@pytest.mark.django_db
def test_comment_contains_correct_data(client):
    """Test that comment response contains all required fields"""
    user = User.objects.create_user(username='testuser', password='testpass')
    project = Project.objects.create(user=user, name='Test Project')
    
    client.force_login(user)
    url = f'/project/project/{project.id}/add-comment/'
    data = {
        'content': 'Testowy komentarz z danymi'
    }
    
    response = client.post(url, json.dumps(data), content_type='application/json')
    
    assert response.status_code == 200
    response_data = json.loads(response.content)
    comment_data = response_data['comment']
    
    assert 'id' in comment_data
    assert 'content' in comment_data
    assert 'author' in comment_data
    assert 'created_at' in comment_data
    assert 'user_id' in comment_data
    assert comment_data['content'] == 'Testowy komentarz z danymi'
    assert comment_data['author'] == user.username
    assert comment_data['user_id'] == user.id


@pytest.mark.django_db
def test_project_detail_shows_existing_comments(client):
    """Test that project detail page shows existing comments"""
    user = User.objects.create_user(username='testuser', password='testpass')
    project = Project.objects.create(user=user, name='Test Project')
    
    # Add some comments to the project
    from project.models import ProjectComment
    comment1 = ProjectComment.objects.create(
        user=user,
        project=project,
        content='Pierwszy komentarz',
        author=user.username
    )
    comment2 = ProjectComment.objects.create(
        user=user,
        project=project,
        content='Drugi komentarz',
        author=user.username
    )
    
    client.force_login(user)
    response = client.get(f'/project/project/{project.id}/')
    
    assert response.status_code == 200
    comments = response.context['comments']
    assert len(comments) == 2
    assert comment1 in comments
    assert comment2 in comments


@pytest.mark.django_db
def test_project_detail_shows_no_comments_message(client):
    """Test that project detail page shows message when no comments exist"""
    user = User.objects.create_user(username='testuser', password='testpass')
    project = Project.objects.create(user=user, name='Test Project')
    
    client.force_login(user)
    response = client.get(f'/project/project/{project.id}/')
    
    assert response.status_code == 200
    comments = response.context['comments']
    assert len(comments) == 0


@pytest.mark.django_db
def test_invalid_json_returns_error(client):
    """Test that invalid JSON in request returns error"""
    user = User.objects.create_user(username='testuser', password='testpass')
    project = Project.objects.create(user=user, name='Test Project')
    
    client.force_login(user)
    url = f'/project/project/{project.id}/add-comment/'
    
    response = client.post(url, 'invalid json', content_type='application/json')
    
    assert response.status_code == 400
    response_data = json.loads(response.content)
    assert 'error' in response_data


@pytest.mark.django_db
def test_nonexistent_project_returns_404(client):
    """Test that trying to add comment to nonexistent project returns 404"""
    user = User.objects.create_user(username='testuser', password='testpass')
    
    client.force_login(user)
    url = '/project/project/999/add-comment/'
    data = {
        'content': 'Test comment'
    }
    
    response = client.post(url, json.dumps(data), content_type='application/json')
    
    assert response.status_code == 404
