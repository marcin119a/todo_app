from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import calendar_view, add_project

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('add/', views.add_task, name='add_task'),
    path('complete/<int:task_id>/', views.complete_task, name='complete_task'),
    path('task/<int:task_id>/', views.task_detail, name='task_detail'),
]

urlpatterns += [
    path('add_project/', add_project, name='add_project'),
]

urlpatterns += [
    path('calendar/', calendar_view, name='calendar'),
]

urlpatterns += [
    path('edit_project/<int:project_id>/', views.edit_project, name='edit_project'),
]

