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

from django.contrib import messages

# the CustomLoginView class is a custom view for user login. It extends Django's built-in LoginView and customizes certain aspects:
# 1. It uses the specified template for rendering the login page.
# 2. It allows all fields to be displayed in the login form.
# 3. If a user is already authenticated, they are redirected to the task list view.
# 4. After successful login, the user is redirected to the task list view using the get_success_url method.

class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__' 
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('tasks')
    

# the RegisterPage class is a view that handles user registration. It uses Django's built-in UserCreationForm for registration, and after successful registration, it logs in the user and redirects them to the task list view. If a user is already authenticated, they are redirected to the task list directly. The get method prevents authenticated users from accessing the registration page again.

class RegisterPage(FormView):
    template_name =  'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')
    
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get( *args, **kwargs)


# the TaskList class is a view that extends Django's built-in ListView and ensures that only logged-in users can access it. It displays a list of tasks, filters them based on the current user and any search input, and provides context data for rendering the template. This class makes it easy to create a task list view with user-specific data and search functionality.

class TaskList(LoginRequiredMixin,ListView):
    model = Task
    context_object_name = 'tasks'
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['tasks'] = data['tasks'].filter(user=self.request.user)
        data['count'] = data['tasks'].filter(complete=False).count()
    
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            data['tasks'] = data['tasks'].filter(
                title__startswith=search_input)
        
        data['search_input'] = search_input
        
        
        return data
    
    

# the TaskDetail class is a view that displays the detailed information of a single task. It enforces that only logged-in users can access it. It utilizes Django's built-in DetailView to render the details of a specific task instance. 

class TaskDetail(LoginRequiredMixin,UserPassesTestMixin,DetailView,PermissionDenied):
    model = Task
    context_object_name = 'tasks'
    template_name = 'base/task.html'
    def test_func(self):
        # Define the conditions for permission based on user roles
        if self.request.user.is_superuser:
            # Admin can create tasks
            return True
        elif self.request.user.groups.filter(name='viewer').exists():
            # viewers can create tasks
            return False
        else:
            return True  # No other users are allowed to create tasks
        # admin yse    viewer no   member yes
    def handle_no_permission(self):
        raise PermissionDenied("You do not have permission to create a task.")

# the TaskCreate class is a view that allows the creation of a new task. It enforces that only logged-in users can access it. It utilizes Django's built-in CreateView to handle the creation process, and specifies the fields that can be set during task creation. After a successful creation, the user is redirected back to the task list view. The form_valid method is overridden to associate the newly created task with the logged-in user.


class TaskCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView,PermissionDenied):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)
    
    def test_func(self):
        # Define the conditions for permission based on user roles
        if self.request.user.is_superuser:
            # Admin can create tasks
            return True
        elif self.request.user.groups.filter(name='viewer').exists():
            # viewers can create tasks
            return True
        else:
            return True  # No other users are allowed to create tasks
        # admin yse    viewer no   member yes
    def handle_no_permission(self):
        raise PermissionDenied("You do not have permission to create a task.")
# the TaskUpdate class is a view that allows the editing and updating of a specific task instance. It enforces that only logged-in users can access it. It utilizes Django's built-in UpdateView to handle the update process and specifies the fields that can be modified in the task instance. After a successful update, the user is redirected back to the task list view.

class TaskUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView,PermissionDenied):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')

    def test_func(self):
        # Define the conditions for permission based on user roles
        if self.request.user.is_superuser:
            # Admin can update tasks
            return True
        elif self.request.user.groups.filter(name='viewer').exists():
            # viewers can create tasks
            return False
        else:
            return True
        # admin yse    viewer no   member yes
# the TaskDeleteView class is a view that allows the deletion of a specific task instance. It enforces that only logged-in users can access it. It uses Django's built-in DeleteView to handle the deletion process and sets the success_url to redirect users back to the task list after a successful deletion.
    def handle_no_permission(self):
        raise PermissionDenied("You do not have permission to create a task.")
    
class DeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView,PermissionDenied):
    model = Task
    context_object_name = 'tasks'
    success_url = reverse_lazy('tasks')
    def test_func(self):
        # Define the conditions for permission based on user roles
        if self.request.user.is_superuser:
            # Admin can delete tasks
            return True
        elif self.request.user.groups.filter(name='viewer').exists():
            # viewers can create tasks
            return False
        else:
            return False  # Other users are not allowed to delete tasks
        # admin yes  viewer no   member no
    def handle_no_permission(self):
        raise PermissionDenied("You do not have permission to create a task.")
    
    
    
    
    
    
    
    # viwers = cacan view task
    
    
    
    
    