import pytest
from django.contrib.auth import get_user_model
from todo.models import Task, Project
from comments.models import Comment

@pytest.mark.django_db
def test_user_can_add_comment_to_task():
    User = get_user_model()
    user = User.objects.create_user(username='testuser', password='testpass')
    project = Project.objects.create(user=user, name='Test Project')
    task = Task.objects.create(user=user, project=project, title='Test Task')
    comment_text = 'To jest komentarz do zadania.'
    comment = Comment.objects.create(user=user, task=task, content=comment_text, author=user.username)
    assert Comment.objects.count() == 1
    assert comment.content == comment_text
    assert comment.task == task
    assert comment.user == user 