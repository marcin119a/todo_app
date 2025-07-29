from rest_framework import serializers
from .models import Comment
from todo.models import Task

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all())

    class Meta:
        model = Comment
        fields = ['id', 'user', 'task', 'content', 'created_at', 'author']

    def update(self, instance, validated_data):
        request = self.context.get('request')
        if request and instance.user != request.user:
            raise serializers.ValidationError('Możesz edytować tylko własne komentarze.')
        return super().update(instance, validated_data)