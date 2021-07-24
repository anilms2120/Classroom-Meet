"""dbms URL Configuration

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
from django.urls import path,include
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
	
    path('admin/', admin.site.urls),
    path('',views.start,name='start'),
    path('view_profile/',views.view_profile,name='view_profile'),
    path('edit_profile/',views.edit_profile,name='edit_profile'),
    path('edit_article/<str:pk>/',views.edit_article,name='edit_article'),
    path('separate_class/<str:pk>/',views.separate_class,name='separate_class'),
    path('edit_assignment/<str:pk>/',views.edit_assignment,name='edit_assignment'),
    path('delete_article/<str:pk>/',views.delete_article,name='delete_article'),
     path('delete_assignment/<str:pk>/',views.delete_assignment,name='delete_assignment'),
    path('view_teacher/<str:pk>/',views.view_teacher,name='view_teacher'),
    path('view_student/<str:pk>/',views.view_student,name='view_student'),
    path('home/',views.home,name='home'),
    path('add_assignment/',views.add_assignment,name='add_assignment'),
    path('create_article/',views.create_article,name='create_article'),
    path('student_assignment/<str:pk>/',views.student_assignment,name='student_assignment'),
    path('all_classes/',views.all_classes,name='all_classes'),
    path('add_class/<str:pk>/',views.add_class,name='add_class'),
    path('remove_class/<str:pk>/',views.remove_class,name='remove_class'),
    path('create_class/',views.create_class,name='create_class'),
    path('student/',views.student_registerpage,name='student_register'),
    path('teacher/',views.teacher_registerpage,name='teacher_register'),
    path('login/',views.loginpage,name='login'),
    path('logout/',views.logoutpage,name='logout'),
]

if settings.DEBUG: 
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
