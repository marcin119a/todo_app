import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from todo.models import Task, Project
from comments.models import Comment

@pytest.mark.django_db
def test_user_can_add_comment_via_api(client):
    User = get_user_model()
    user = User.objects.create_user(username='apitestuser', password='testpass')
    project = Project.objects.create(user=user, name='API Project')
    task = Task.objects.create(user=user, project=project, title='API Task')
    url = '/comments/add/'
    data = {
        'user_id': user.id,
        'task_id': task.id,
        'content': 'Komentarz przez API'
    }
    response = client.post(url, data, content_type='application/json')
    assert response.status_code == 200
    resp_json = response.json()
    assert resp_json['content'] == 'Komentarz przez API'
    assert resp_json['task'] == task.id
    assert resp_json['user'] == user.id
    assert Comment.objects.filter(task=task, user=user, content='Komentarz przez API').exists() 