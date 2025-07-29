from django.urls import path
from .views import add_project, AddMemberAPIView, calendar_view, edit_project, project_list


urlpatterns = [
    path('add_project/', add_project, name='add_project'),
    path('api/<int:pk>/add-member/', AddMemberAPIView.as_view(), name='api_add_member'),
]

urlpatterns += [
    path('calendar/', calendar_view, name='calendar'),
]

urlpatterns += [
    path('edit_project/<int:project_id>/',edit_project, name='edit_project'),
]

urlpatterns += [
    path('projects/', project_list, name='project_list'),
]
