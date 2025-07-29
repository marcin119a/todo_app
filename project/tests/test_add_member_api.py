import pytest
from django.contrib.auth import get_user_model
from project.models import Project

@pytest.mark.django_db
def test_owner_can_add_member_to_project(client):
    User = get_user_model()
    owner = User.objects.create_user(username='owner', password='pass')
    invited = User.objects.create_user(username='invited', password='pass')
    project = Project.objects.create(user=owner, name='Test Project')
    client.force_login(owner)
    url = f'/project/api/{project.id}/add-member/'
    response = client.post(url, {'username': invited.username}, content_type='application/json')
    assert response.status_code == 200
    project.refresh_from_db()
    assert invited in project.members.all() 