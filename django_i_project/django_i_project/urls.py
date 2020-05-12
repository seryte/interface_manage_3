"""django_i_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from interface_app.views import user_views
from interface_app.views.interface.interface_detail import InterfaceDetailView
from interface_app.views.interface.interface_list import InterfaceListView
from interface_app.views.service.service_detail import ServiceDetailView
from interface_app.views.service.service_list import ServiceListView
from interface_app.views.task.task_detail import TaskDetailView
from interface_app.views.task.task_list import TaskListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/login/', user_views.user_login),
    path('user/register/', user_views.user_register),
    path('user/logout/', user_views.user_logout),
    path('user/info/', user_views.get_user_info),

    path("api/services/", ServiceListView.as_view()),
    path("api/service/<int:base_id>/", ServiceDetailView.as_view()),

    path("api/tasks/", TaskListView.as_view()),
    path("api/task/<int:base_id>/", TaskDetailView.as_view()),

    path("api/interfaces/", InterfaceListView.as_view()),
    path("api/interface/<int:base_id>/", InterfaceDetailView.as_view()),
]
