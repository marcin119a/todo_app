import pytest
from django.core import mail
from django.contrib.auth import get_user_model
from todo.models import Task, Tag, Project
from todo.tasks import send_task_reminder_email
from datetime import timedelta
from django.utils import timezone

@pytest.fixture
def user(db):
    User = get_user_model()
    return User.objects.create_user(username='testuser', email='test@example.com', password='testpass')

@pytest.fixture
def project(db):
    return Project.objects.create(name='Test Project')

@pytest.fixture
def tag(db):
    return Tag.objects.create(name='Test Tag')

@pytest.fixture
def task(db, user, project, tag):
    t = Task.objects.create(
        title='Test Task',
        project=project,
        completed=False,
        priority=1,
        due_date=timezone.now() + timedelta(hours=1),
    )
    t.user = user
    t.save()
    t.tags.add(tag)
    return t

def test_send_task_reminder_email(task):
    send_task_reminder_email(task)
    assert len(mail.outbox) == 1
    email = mail.outbox[0]
    assert 'Test Task' in email.body
    assert task.user.email in email.recipients() 