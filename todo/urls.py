from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import task_list, add_task, complete_task, task_detail, TaskDeleteView, TaskUpdateView
from .views import api_tags

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('add/', views.add_task, name='add_task'),
    path('complete/<int:task_id>/', views.complete_task, name='complete_task'),
    path('task/<int:task_id>/', views.task_detail, name='task_detail'),
    path('api/tags/', api_tags, name='api_tags'),
]

urlpatterns += [
    path('delete_task/<int:pk>/', TaskDeleteView.as_view(), name='delete_task'),
    path('edit_task/<int:task_id>/', TaskUpdateView.as_view(), name='edit_task'),
]
