from django.urls import path
from .views import ProjectCreateView, AddMemberAPIView, calendar_view, ProjectUpdateView, project_list


urlpatterns = [
    path('add_project/', ProjectCreateView.as_view(), name='add_project'),
    path('api/<int:pk>/add-member/', AddMemberAPIView.as_view(), name='api_add_member'),
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
