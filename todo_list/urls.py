
# from django.contrib import admin
# from django.urls import path, include

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('',include('base.urls'))
# ]



# from django.contrib import admin
# from django.urls import path, include
# from base.admin import Task_site

# from rest_framework.routers import DefaultRouter
# from base.views import CustomLoginView, RegisterPage


# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('',include('base.urls')),
#     path('Taskadmin/', Task_site.urls)
# ]

from django.contrib import admin
from django.urls import path, include
# from base.views import TaskViewSet



urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('', include('base.urls')),
]
