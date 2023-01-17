"""SubHazProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from SubHazApp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='home'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('client/', client, name='client'),

    path('consultant/<str:name>/', contractor, name='contractor'),
    path('consultants/', contractors, name='contractors'),

    path('work/', work, name='work'),

    path('search/', search, name='search'),

    path('unavailability/', unavailability, name='unavailability'),
    path('choice/', choice, name='choice'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', register_user, name='register'),
    path('register-consultant/', register_consultant, name='register_consultant'),
    path('register-company/', register_company, name='register_company'),
    path('certificate/', certificate, name='certificate'),

    path('blog/', blog, name='blog'),
    path('posts/<slug:slug>/', post_details, name='post_details'),


    path('job-offers/', job_offers, name='job-offers'),
	path('uploadfile/', upload_file, name='upload-file'),
    path('tinymce/', include('tinymce.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
