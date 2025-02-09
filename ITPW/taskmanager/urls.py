from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('projects/', views.project_list, name='project_list'),
    path('project/<int:pk>/', views.project_detail, name='project_detail'),
    path('task/<int:pk>/', views.task_detail, name='task_detail'),
    path('login/', auth_views.LoginView.as_view(
        template_name='taskmanager/login.html',
        redirect_authenticated_user=True
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('project/new/', views.project_create, name='project_create'),
    path('project/<int:pk>/edit/', views.project_update, name='project_update'),
    path('project/<int:project_pk>/task/new/', views.task_create, name='task_create_for_project'),
    path('task/new/', views.task_create, name='task_create'),
    path('task/<int:pk>/edit/', views.task_update, name='task_update'),
    path('project/<int:pk>/delete/', views.project_delete, name='project_delete'),
    path('task/<int:pk>/delete/', views.task_delete, name='task_delete'),
    path('tasks/', views.task_list, name='task_list'),
    path('profile/', views.profile, name='profile'),
    path('project/<int:pk>/update-status/', views.project_update_status, name='project_update_status'),
]
