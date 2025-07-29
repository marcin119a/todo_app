from django.urls import path
from django.contrib.auth import views as auth_views
from user.views import login_view, logout_view, register, account_summary, edit_account

urlpatterns = []

urlpatterns += [
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='user/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='user/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='user/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='user/password_reset_complete.html'), name='password_reset_complete'),
]
urlpatterns += [
    path('login/', login_view, name='login'),
    path('register/', register, name='register'),
    path('account_summary/', account_summary, name='account_summary'),
    path('edit/', edit_account, name='edit_account'),
]

urlpatterns += [
    path('logout/', logout_view, name='logout'),
]
urlpatterns += [
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='user/password_change_form.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='user/password_change_done.html'), name='password_change_done'),
]
