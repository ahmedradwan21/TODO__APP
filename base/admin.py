# from django.contrib import admin
# from .models import Task

# admin.site.register(Task)



from django.contrib import admin
from django.http.request import HttpRequest
from .models import Task
from . import models

admin.site.register(Task)

class TaskAdminArea(admin.AdminSite):
    site_header = 'Task Admin Database'
    

class TestAdminPermission(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False


Task_site = TaskAdminArea(name= 'Task_Admin')

Task_site.register(models.Task,TestAdminPermission)


