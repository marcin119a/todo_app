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


class ProjectComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='project_comments', null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Komentarz do projektu: {self.project.name} ({self.created_at:%Y-%m-%d %H:%M})"

    class Meta:
        ordering = ['-created_at']
