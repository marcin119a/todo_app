from django.urls import path
from .views import ProjectCreateView, AddMemberAPIView, calendar_view, ProjectUpdateView, project_list, project_detail, add_project_comment


urlpatterns = [
    path('add_project/', ProjectCreateView.as_view(), name='add_project'),
    path('api/<int:pk>/add-member/', AddMemberAPIView.as_view(), name='api_add_member'),
    path('project/<int:project_id>/', project_detail, name='project_detail'),
    path('project/<int:project_id>/add-comment/', add_project_comment, name='add_project_comment'),
]

urlpatterns += [
    path('calendar/', calendar_view, name='calendar'),
]

urlpatterns += [
    path('edit_project/<int:project_id>/', ProjectUpdateView.as_view(), name='edit_project'),
]

urlpatterns += [
    path('projects/', project_list, name='project_list'),
]
