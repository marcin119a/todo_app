import pytest
from django.contrib.auth import get_user_model
from todo.models import Task, Project
from comments.models import Comment

@pytest.mark.django_db
def test_user_can_delete_own_comment(client):
    User = get_user_model()
    user = User.objects.create_user(username='deletecommentuser', password='testpass')
    project = Project.objects.create(user=user, name='Delete Comment Project')
    task = Task.objects.create(user=user, project=project, title='Task for Comment')
    comment = Comment.objects.create(user=user, task=task, content='Do usunięcia', author=user.username)
    client.force_login(user)
    url = f'/comments/api/delete/{comment.id}/'
    response = client.delete(url)
    assert response.status_code == 200
    assert not Comment.objects.filter(id=comment.id).exists() 