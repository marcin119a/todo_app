from .models import Project
from django.contrib import admin

# Register your models here.

class ProjectAdmin(admin.ModelAdmin):
    filter_horizontal = ('members',)

admin.site.register(Project, ProjectAdmin)
