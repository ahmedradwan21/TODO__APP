from django.urls import path
from django.contrib import admin
from .views import TaskList, TaskDetail, TaskCreate, TaskUpdate ,DeleteView,CustomLoginView,RegisterPage
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('login/',CustomLoginView.as_view(), name='login'),
    path('logout/',LogoutView.as_view(next_page='login'), name='logout'),
    path('register/',RegisterPage.as_view() ,name='register'),
    path('',TaskList.as_view(), name='tasks'),
    path('task/<int:pk>/', TaskDetail.as_view(), name='task'),
    path('task-create/', TaskCreate.as_view(), name='task-create'),
    path('task-update/<int:pk>/', TaskUpdate.as_view(), name='task-update'),
    path('task-delete/<int:pk>/', DeleteView.as_view(), name='task-delete'),
]

admin.site.index_title = 'Ahmed Tarek Radwan(ATR) 🦅 & Dragons 🐉'
admin.site.site_header = 'Dragons 🐉'
admin.site.site_title = "TODO_LIST_APP 🦅 "