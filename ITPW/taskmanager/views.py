from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DeleteView
from .models import Project, Task, Comment
from .forms import ProjectForm, TaskForm, CommentForm
from django.contrib.auth.models import User
from django.db.models import Count, Avg, Q, F, ExpressionWrapper, FloatField
from django.db.models.functions import ExtractWeek, Now
from django.utils import timezone
import json
from django.core.paginator import Paginator

@login_required
def index(request):
    """Root path redirects to dashboard if authenticated"""
    return redirect('dashboard')

@login_required
def dashboard(request):
    user_projects = Project.objects.filter(team_members=request.user).prefetch_related('tasks')
    user_tasks = Task.objects.filter(assigned_to=request.user)
    
    # Project statistics by status
    project_stats = {status[0]: user_projects.filter(status=status[0]).count() 
                    for status in Project.STATUS_CHOICES}
    
    # Task statistics by status
    task_stats = {status[0]: user_tasks.filter(status=status[0]).count() 
                 for status in Task.STATUS_CHOICES}
    
    # Completion statistics
    completion_stats = {
        'completed_projects': user_projects.filter(status='COMPLETED').count(),
        'completed_tasks': user_tasks.filter(status='DONE').count(),
        'completion_rate': round((user_tasks.filter(status='DONE').count() / user_tasks.count() * 100) 
                               if user_tasks.count() > 0 else 0),
        'total_projects': user_projects.count(),
    }
    
    context = {
        'project_stats': project_stats,
        'task_stats': task_stats,
        'completion_stats': completion_stats,
        'projects': user_projects,
        'tasks': user_tasks.order_by('due_date')[:5],
    }
    return render(request, 'taskmanager/dashboard.html', context)

@login_required
def project_list(request):
    projects = Project.objects.filter(team_members=request.user)
    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category', '')
    
    if search_query:
        projects = projects.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    if category_filter:
        projects = projects.filter(category=category_filter)
        
    return render(request, 'taskmanager/project_list.html', {
        'projects': projects,
        'search_query': search_query,
        'category_filter': category_filter,
    })

@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    tasks = Task.objects.filter(project=project)
    return render(request, 'taskmanager/project_detail.html', {'project': project, 'tasks': tasks})

@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    comments = Comment.objects.filter(task=task)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = task
            comment.author = request.user
            comment.save()
            return redirect('task_detail', pk=pk)
    else:
        form = CommentForm()
    return render(request, 'taskmanager/task_detail.html', 
                 {'task': task, 'comments': comments, 'form': form})

@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.manager = request.user
            project.save()
            project.team_members.add(request.user)  # Add creator to team members
            messages.success(request, 'Project created successfully!')
            return redirect('dashboard')
    else:
        form = ProjectForm()
    
    return render(request, 'taskmanager/project_form.html', {
        'form': form,
        'action': 'Create'
    })

@login_required
def project_update(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project updated successfully!')
            return redirect('project_detail', pk=pk)
    else:
        form = ProjectForm(instance=project)
    return render(request, 'taskmanager/project_form.html', {'form': form, 'action': 'Update'})

@login_required
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Project deleted successfully!')
        return redirect('project_list')
    return render(request, 'taskmanager/project_confirm_delete.html', {'project': project})

@login_required
def project_update_status(request, pk):
    if request.method == 'POST':
        project = get_object_or_404(Project, pk=pk)
        new_status = request.POST.get('status')
        if new_status and new_status in dict(Project.STATUS_CHOICES):
            project.status = new_status
            project.save()
            messages.success(request, f'Project status updated to {project.get_status_display()}')
        return redirect('project_detail', pk=pk)
    return redirect('project_list')

@login_required
def task_create(request, project_pk=None):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.save()
            messages.success(request, 'Task created successfully!')
            return redirect('task_detail', pk=task.pk)
    else:
        initial = {}
        if project_pk:
            initial['project'] = get_object_or_404(Project, pk=project_pk)
        form = TaskForm(initial=initial)
    return render(request, 'taskmanager/task_form.html', {'form': form, 'action': 'Create'})

@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully!')
            return redirect('task_detail', pk=pk)
    else:
        form = TaskForm(instance=task)
    return render(request, 'taskmanager/task_form.html', {'form': form, 'action': 'Update'})

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        project = task.project
        task.delete()
        messages.success(request, 'Task deleted successfully!')
        return redirect('project_detail', pk=project.pk)
    return render(request, 'taskmanager/task_confirm_delete.html', {'task': task})

@login_required
def task_list(request):
    status_filter = request.GET.get('status', '')
    priority_filter = request.GET.get('priority', '')
    search_query = request.GET.get('search', '')
    sort_by = request.GET.get('sort_by', 'due_date')
    
    tasks = Task.objects.filter(assigned_to=request.user)
    
    if status_filter:
        tasks = tasks.filter(status=status_filter)
    if priority_filter:
        tasks = tasks.filter(priority=priority_filter)
    if search_query:
        tasks = tasks.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Sorting
    valid_sort_fields = ['due_date', '-due_date', 'priority', '-priority', 'status', '-status']
    if sort_by in valid_sort_fields:
        tasks = tasks.order_by(sort_by)
    else:
        tasks = tasks.order_by('due_date')
    
    # Pagination
    paginator = Paginator(tasks, 10)
    page_number = request.GET.get('page', 1)
    tasks_page = paginator.get_page(page_number)
    
    context = {
        'tasks': tasks_page,
        'status_filter': status_filter,
        'priority_filter': priority_filter,
        'search_query': search_query,
        'sort_by': sort_by,
        'status_choices': Task.STATUS_CHOICES,
        'priority_choices': Task.PRIORITY_CHOICES
    }
    return render(request, 'taskmanager/task_list.html', context)

@login_required
def profile(request):
    return render(request, 'taskmanager/profile.html', {
        'user': request.user
    })

@login_required
def settings(request):
    return render(request, 'taskmanager/settings.html', {
        'user': request.user
    })
