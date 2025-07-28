from django.urls import path
from . import views
from .views import register
from .views import login_view
from .views import logout_view
from .views import add_project
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('add/', views.add_task, name='add_task'),
    path('complete/<int:task_id>/', views.complete_task, name='complete_task'),
    path('task/<int:task_id>/', views.task_detail, name='task_detail'),
    path('register/', register, name='register'),
]

urlpatterns += [
    path('login/', login_view, name='login'),
]

urlpatterns += [
    path('logout/', logout_view, name='logout'),
]

urlpatterns += [
    path('add_project/', add_project, name='add_project'),
]

urlpatterns += [
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='todo/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='todo/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='todo/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='todo/password_reset_complete.html'), name='password_reset_complete'),
]