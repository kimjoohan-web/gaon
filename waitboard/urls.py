from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'waitboard'
urlpatterns =[
    path('', views.wait, name='wait'),  
    path('wait_create/', views.wait_create, name='wait_create'),       
    path('wait_detail/<int:w_id>/', views.wait_detail, name='wait_detail'),
    path('wait_modify/<int:w_id>/', views.wait_modify, name='wait_modify'),
    path('wait_delete/<int:w_id>/', views.wait_delete, name='wait_delete'),
]
