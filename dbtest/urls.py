from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'dbtest'
urlpatterns =[   
    
    path('', views.dbtest,name='dbtest'),            
    path('db_create/', views.db_create, name='db_create'), 
    path('<int:dbtest_id>/', views.db_detail, name='db_detail'),
    
]
