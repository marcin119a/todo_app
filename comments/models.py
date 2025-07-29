from django.db import models
from django.contrib.auth import get_user_model
from todo.models import Task

User = get_user_model()

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Komentarz do: {self.task.title} ({self.created_at:%Y-%m-%d %H:%M})"
