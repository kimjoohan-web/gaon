from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'cale'
urlpatterns =[
    
    path('', views.cale_list,name='cale_list'), 
    
    
    
    
]
