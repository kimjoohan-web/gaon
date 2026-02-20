"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from pybo.views import base_views
from main import views
from django.conf import settings
from config.settings.base import *
from django.conf.urls.static import static
from django.views.static import serve
from django.urls import re_path
# from pybo import views
urlpatterns = [
    path('summernote/', include('django_summernote.urls')),
    path('admin/', admin.site.urls),
    path('pybo/', include('pybo.urls')),
    path('common/', include('common.urls')),
    # path('', base_views.index, name='index'),  # '/' 에 해당되는 path
    path('categoryView/', base_views.categoryView, name='categoryView'),  # '/' 에 해당되는 path
    # path ('', include('main.urls')), # 메인 페이지
    path ('', views.index, name='index'), # 메인 페이지
    path('board/', include('board.urls')),
    # path('pybo/', include('pybo.urls')),
    path('chat/', include('chat.urls')),
    path('cale/', include('cale.urls')),
    path('gaonsample/', include('gaonsample.urls')),
    path('mt/', include('mt.urls')),
    path('manager/', include('manager.urls')),
    path('psecu/', include('psecu.urls')),
    path('gdraft/', include('gdraft.urls')),
    path('aisample/', include('aisample.urls')),
    path('gchat/', include('gchat.urls')),
    path('vaca/', include('vaca.urls')),
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



def get_filename(filename):
    return filename.upper()