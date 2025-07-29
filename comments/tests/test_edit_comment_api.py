import pytest
from django.contrib.auth import get_user_model
from todo.models import Task, Project
from comments.models import Comment

@pytest.mark.django_db
def test_user_can_edit_own_comment(client):
    User = get_user_model()
    user = User.objects.create_user(username='editcommentuser', password='testpass')
    project = Project.objects.create(user=user, name='Edit Comment Project')
    task = Task.objects.create(user=user, project=project, title='Task for Edit')
    comment = Comment.objects.create(user=user, task=task, content='Stara treść', author=user.username)
    client.force_login(user)
    url = f'/comments/api/edit/{comment.id}/'
    new_content = 'Nowa treść komentarza'
    response = client.put(url, {'content': new_content}, content_type='application/json')
    assert response.status_code == 200
    comment.refresh_from_db()
    assert comment.content == new_content 