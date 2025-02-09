from django.contrib import admin
from .models import Project, Task, Comment

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('status', 'created_at')

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'assigned_to', 'status', 'priority', 'due_date')
    search_fields = ('title', 'description')
    list_filter = ('status', 'priority', 'due_date')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('task', 'author', 'created_at')
    search_fields = ('content',)
    list_filter = ('created_at',)
