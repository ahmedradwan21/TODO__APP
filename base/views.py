import datetime
from typing import Any, Dict
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView , UpdateView , DeleteView ,FormView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth import login
from base.admin import TestAdminPermission 
from .models import Task



from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import Group
from django.contrib import messages





# the CustomLoginView class is a custom view for user login. It extends Django's built-in LoginView and customizes certain aspects:
# 1. It uses the specified template for rendering the login page.
# 2. It allows all fields to be displayed in the login form.
# 3. If a user is already authenticated, they are redirected to the task list view.
# 4. After successful login, the user is redirected to the task list view using the get_success_url method.


from django.contrib.auth.views import LoginView
from django.contrib.auth import login

class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__' 
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')



class RegisterPage(FormView):
    template_name =  'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')
    
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            group_name = self.request.POST.get('groups', 'Viewerr')
            try:
                group = Group.objects.get(name=group_name)
                user.groups.add(group)
            
            except Group.DoesNotExist:
                pass
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get( *args, **kwargs)


# -----------------------------------------------------

# from rest_framework import viewsets
# from .models import Task
# from .serializers import TaskSerializer

# class TaskViewSet(viewsets.ModelViewSet):
#     queryset = Task.objects.all()
#     serializer_class = TaskSerializer

# from rest_framework import generics
# from django.db.models import Q
# from .models import Task
# from .serializers import TaskSerializer

# class TaskFilterView(generics.ListAPIView):
#     serializer_class = TaskSerializer

#     def get_queryset(self):
#         status = self.request.query_params.get('status', '')  
#         if status.lower() == 'complete':
#             return Task.objects.filter(complete=True)
#         elif status.lower() == 'incomplete':
#             return Task.objects.filter(complete=False)
#         return Task.objects.all()

# base/views.py
# from rest_framework import generics
# from rest_framework.permissions import IsAuthenticated
# from .models import Task
# from .serializers import TaskSerializer
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status

# class TaskListAPIView(generics.ListCreateAPIView):
#     queryset = Task.objects.all()
#     serializer_class = TaskSerializer


# class TaskDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = TaskSerializer
#     queryset = Task.objects.all()

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Task
from .serializers import TaskSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.views import TokenObtainPairView

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = TaskSerializer

class TodoListApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        todos = Task.objects.filter(user=request.user)
        serializer = TaskSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        fields = ["user", "title", "description", "created", "complete"]
        data = {
                'title': request.data.get('title'),  # Use 'title' instead of 'task'
                'description': request.data.get('description'),
                'created': datetime.now(),  # You need to set the 'created' field properly
                'complete': request.data.get('completed'),
                'user': request.user.id
            }
        serializer = TaskSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# -----------------------------------------------------


class TaskList(LoginRequiredMixin,ListView):
    model = Task
    context_object_name = 'tasks'
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['tasks'] = data['tasks'].filter(user=self.request.user)
        data['count'] = data['tasks'].filter(complete=False).count()
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            data['tasks'] = data['tasks'].filter(title__startswith=search_input)
            data['search_input'] = search_input
        return data
    


class TaskDetail(LoginRequiredMixin,UserPassesTestMixin,DetailView,PermissionDenied):
    model = Task
    context_object_name = 'tasks'
    template_name = 'base/task.html'
    def test_func(self):
        if self.request.user.is_superuser:
            return True
        elif self.request.user.groups.filter(name='Viewer').exists():
            return False
        elif self.request.user.groups.filter(name='Member').exists():
            return True
        else:
            return True  
        # admin yse    viewer no   member yes
    def handle_no_permission(self):
        raise PermissionDenied("You do not have permission to create a task.")


class TaskCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView,PermissionDenied):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)
    
    def test_func(self):
        if self.request.user.is_superuser:
            return True
        elif self.request.user.groups.filter(name='Viewer').exists():
            return True
        elif self.request.user.groups.filter(name='Member').exists():
            return True
        else:
            return True  
        # admin yse    viewer no   member yes
    def handle_no_permission(self):
        raise PermissionDenied("You do not have permission to create a task.")



class TaskUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView,PermissionDenied):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')
    def test_func(self):
        
        if self.request.user.is_superuser:
            return True
        elif self.request.user.groups.filter(name='Viewer').exists():
            return False
        elif self.request.user.groups.filter(name='Member').exists():
            return True
        else:
            return True
        # admin yse    viewer no   member yes
    def handle_no_permission(self):
        raise PermissionDenied("You do not have permission to create a task.")
    
    

class DeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView,PermissionDenied):
    model = Task
    context_object_name = 'tasks'
    success_url = reverse_lazy('tasks')
    def test_func(self):
        if self.request.user.is_superuser:
            return True
        elif self.request.user.groups.filter(name='Viewer').exists():
            return False
        elif self.request.user.groups.filter(name='Member').exists():
            return False
        else:
            return False  
        # admin yes  viewer no   member no
    def handle_no_permission(self):
        raise PermissionDenied("You do not have permission to create a task.")
    
    
    
    
    
    
    
    # viwers = cacan view task
    
    
    
    
    