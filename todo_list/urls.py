
# from django.contrib import admin
# from django.urls import path, include

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('',include('base.urls'))
# ]



from django.contrib import admin
from django.urls import path, include
from base.admin import Task_site

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('base.urls')),
    path('Taskadmin/', Task_site.urls)
]
