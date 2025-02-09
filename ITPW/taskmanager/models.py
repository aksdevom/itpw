from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from .constants import *

class Project(models.Model):
    STATUS_CHOICES = PROJECT_STATUS_CHOICES
    PRIORITY_CHOICES = PRIORITY_CHOICES
    CATEGORY_CHOICES = CATEGORY_CHOICES

    name = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name='managed_projects')
    team_members = models.ManyToManyField(User, related_name='project_teams')
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='OTHER')
    status = models.CharField(max_length=20, choices=PROJECT_STATUS_CHOICES, default='PLANNING')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='MEDIUM')

    def __str__(self):
        return self.name

    def get_status_display(self):
        return dict(self.STATUS_CHOICES)[self.status]

    class Meta:
        ordering = ['-created_at']

class Task(models.Model):
    STATUS_CHOICES = STATUS_CHOICES
    PRIORITY_CHOICES = PRIORITY_CHOICES

    title = models.CharField(max_length=200)
    description = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_tasks')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='TODO')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='MEDIUM')
    due_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    labels = models.CharField(max_length=200, blank=True, help_text="Comma-separated labels")
    estimated_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    actual_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    dependencies = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='dependent_tasks')
    
    def __str__(self):
        return self.title

    def get_labels_list(self):
        return [label.strip() for label in self.labels.split(',') if label.strip()]

    def can_start(self):
        """Check if all dependencies are completed"""
        return all(dep.status == 'DONE' for dep in self.dependencies.all())

    class Meta:
        ordering = ['-created_at']

class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.task.title}'

class Activity(models.Model):
    ACTION_CHOICES = [
        ('CREATE', 'Created'),
        ('UPDATE', 'Updated'),
        ('DELETE', 'Deleted'),
        ('COMMENT', 'Commented'),
        ('STATUS', 'Changed Status'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    target_type = models.CharField(max_length=20)  # 'project' or 'task'
    target_id = models.IntegerField()
    details = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
