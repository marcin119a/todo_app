from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from todo.models import Task
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import CommentSerializer
from rest_framework.generics import get_object_or_404
from comments.models import Comment


class AddCommentAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user, author=request.user.username)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EditCommentAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, pk, format=None):
        comment = get_object_or_404(Comment, pk=pk)
        serializer = CommentSerializer(comment, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteCommentAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk, format=None):
        comment = get_object_or_404(Comment, pk=pk)
        if comment.user != request.user:
            return Response({'error': 'Możesz usunąć tylko własny komentarz.'}, status=status.HTTP_403_FORBIDDEN)
        comment.delete()
        return Response({'success': True})
