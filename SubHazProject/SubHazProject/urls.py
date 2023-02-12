from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from SubHazApp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='home'),
    path('subscriptions', subscriptions, name='about'),

    path('clanovi/', contractors, name='contractors'),
    
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', register_user, name='register'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
