
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
from rest_framework.routers import DefaultRouter
from base.views import CustomLoginView, RegisterPage
from base.views import TaskViewSet

# Create a router for the API views
router = DefaultRouter()
router.register(r'todos', TaskViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', RegisterPage.as_view(), name='register'),
    path('api/', include(router.urls)),  # Include the API endpoints
    path('', include('base.urls')),
]
