from django.urls import path
from django.contrib import admin
from .views import TaskList, TaskDetail, TaskCreate, TaskUpdate ,DeleteView,CustomLoginView,RegisterPage
from django.contrib.auth.views import LogoutView
from . import views
from .views import (TodoListApiView,CustomTokenObtainPairView)

urlpatterns = [
    path('login/',CustomLoginView.as_view(), name='login'),
    path('logout/',LogoutView.as_view(next_page='login'), name='logout'),
    path('register/',RegisterPage.as_view() ,name='register'),
    path('api/tasks/',TaskList.as_view(), name='tasks'),
    path('api/tasks/<int:pk>/', TaskDetail.as_view(), name='task'),
    path('api/tasks/create/', TaskCreate.as_view(), name='task-create'),
    path('api/tasks/<int:pk>/update/', TaskUpdate.as_view(), name='task-update'),
    path('api/tasks/<int:pk>/delete/', DeleteView.as_view(), name='task-delete'),
    # path('api/taskss/', views.TaskListAPIView.as_view(), name='api-task-list'),
    # path('api/tasks/<int:pk>/', views.TaskDetailAPIView.as_view(), name='api-task-detail'),
    path('custmam-token/', CustomTokenObtainPairView.as_view(), name='custom-token'),
    path('api/', TodoListApiView.as_view(), name='api-todo-list'),
]

admin.site.index_title = 'Ahmed Tarek Radwan(ATR) 🦅 & Dragons 🐉'
admin.site.site_header = 'Dragons 🐉'
admin.site.site_title = "TODO_LIST_APP 🦅 "