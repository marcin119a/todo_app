from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import task_list, add_task, complete_task, task_detail, TaskDeleteView

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('add/', views.add_task, name='add_task'),
    path('complete/<int:task_id>/', views.complete_task, name='complete_task'),
    path('task/<int:task_id>/', views.task_detail, name='task_detail'),
]

urlpatterns += [
    path('delete_task/<int:pk>/', TaskDeleteView.as_view(), name='delete_task'),
]



