from django.urls import path
from django.contrib import admin
from .views import TaskList, TaskDetail, TaskCreate, TaskUpdate ,DeleteView,CustomLoginView,RegisterPage,TaskFilterView
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('login/',CustomLoginView.as_view(), name='login'),
    path('logout/',LogoutView.as_view(next_page='login'), name='logout'),
    path('register/',RegisterPage.as_view() ,name='register'),
    path('api/tasks/',TaskList.as_view(), name='tasks'),
    path('api/tasks/<int:pk>/', TaskDetail.as_view(), name='task'),
    path('api/tasks/create/', TaskCreate.as_view(), name='task-create'),
    path('api/tasks/<int:pk>/update/', TaskUpdate.as_view(), name='task-update'),
    path('api/tasks/<int:pk>/delete/', DeleteView.as_view(), name='task-delete'),
    path('api/tasks/filter/', TaskFilterView.as_view(), name='tasks-filter'),
]

admin.site.index_title = 'Ahmed Tarek Radwan(ATR) 🦅 & Dragons 🐉'
admin.site.site_header = 'Dragons 🐉'
admin.site.site_title = "TODO_LIST_APP 🦅 "