from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects', null=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    members = models.ManyToManyField(User, related_name='shared_projects', blank=True)

    def __str__(self):
        return self.name
