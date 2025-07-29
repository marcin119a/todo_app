from django.urls import path
from . import views
from .views import AddCommentAPIView, EditCommentAPIView, DeleteCommentAPIView

urlpatterns = [
    path('api/add/', AddCommentAPIView.as_view(), name='api_add_comment'),
    path('api/edit/<int:pk>/', EditCommentAPIView.as_view(), name='api_edit_comment'),
    path('api/delete/<int:pk>/', DeleteCommentAPIView.as_view(), name='api_delete_comment'),
] 