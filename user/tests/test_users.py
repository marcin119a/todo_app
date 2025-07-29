import pytest
from django.core import mail
from django.contrib.auth import get_user_model
from todo.models import Task, Tag, Project, Comment
from todo.tasks import send_task_reminder_email
from datetime import timedelta
from django.utils import timezone
from django.urls import reverse


@pytest.mark.django_db
def test_login_and_task_list(client):
    User = get_user_model()
    # Create user and task
    user, _ = User.objects.get_or_create(username='testuser2', email='test_2@example.com', password='testpass123@')
    task = Task.objects.get_or_create(title='Moje zadanie', user=user)

    # Login
    login_url = reverse('login')
    response = client.post(login_url, {'email': 'test_2@example.com', 'password': 'testpass123'}, follow=True)
    assert response.status_code == 200
    # After login, redirect to task list
    assert 'Twoje zadania' in response.content.decode()
    # Check if task is visible
    assert 'Moje zadanie' in response.content.decode()

@pytest.mark.django_db
def test_password_reset_email(client):
    User = get_user_model()
    # Create user
    user, _ = User.objects.get_or_create(username='testuser', email='test@example.com', password='testpass123')

    reset_url = reverse('password_reset')
    response = client.post(reset_url, {'email': 'test@example.com'}, follow=True)
    assert response.status_code == 200
    # Check confirmation message on page
    assert 'Wysłaliśmy instrukcje dotyczące resetu hasła' in response.content.decode()
    # Check that an email was sent
    assert len(mail.outbox) == 1
    assert 'test@example.com' in mail.outbox[0].to
    assert 'reset' in mail.outbox[0].body or 'reset' in mail.outbox[0].subject 


@pytest.mark.django_db
def test_password_change(client):
    User = get_user_model()
    User.objects.filter(username='test21321').delete()
    user = User.objects.create(username='test21321', email='test21321@example.com', password='oldpass123')
    client.login(username='test21321', password='oldpass123')
    url = reverse('password_change')
    response = client.post(url, {
        'old_password': 'oldpass123',
        'new_password1': 'newpass456!',
        'new_password2': 'newpass456!',
    }, follow=True)
    assert response.status_code == 200
    assert 'Hasło zostało zmienione' in response.content.decode()
    print(response.content.decode())
    # Wylogowanie i próba logowania nowym hasłem
    client.logout()
    login_url = reverse('login')
    response = client.post(login_url, {'email': 'user_test_password_change_2@example.com', 'password': 'newpass456!'}, follow=True)
    assert response.status_code == 200
    assert 'Twoje zadania' in response.content.decode() 


@pytest.mark.django_db
def test_account_summary_view(client):
    User = get_user_model()
    user, _ = User.objects.get_or_create(username='testuser', email='test@example.com', password='testpass123')
    client.force_login(user)
    # Create projects and tasks
    project1 = Project.objects.create(name='Projekt 1', user=user)
    project2 = Project.objects.create(name='Projekt 2', user=user)
    today = timezone.now().date()
    Task.objects.create(title='Zadanie ukończone', user=user, completed=True, due_date=today)
    Task.objects.create(title='Zadanie zaległe', user=user, completed=False, due_date=today - timedelta(days=2))
    Task.objects.create(title='Zadanie zbliżające się', user=user, completed=False, due_date=today + timedelta(days=2))
    Task.objects.create(title='Zadanie inne', user=user, completed=False, due_date=today + timedelta(days=10))

    url = reverse('account_summary')
    response = client.get(url)
    assert response.status_code == 200
    content = response.content.decode()
    # Check projects
    assert 'Projekt 1' in content
    assert 'Projekt 2' in content
    # Check statistics
    assert 'Wszystkie zadania: 4' in content
    assert 'Ukończone: 1' in content
    assert 'Zaległe: 1' in content
    assert 'Zbliżające się (3 dni): 1' in content 

