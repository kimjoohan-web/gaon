from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'f_board'
urlpatterns =[
    
    path('f_create/', views.f_create,name='f_create'), 
    path('', views.f_list,name='f_list'),     
    path('<int:f_board_id>/', views.f_detail,name='f_detail'),    
    path('f_modify/<int:f_board_id>/', views.f_modify,name='f_modify'),    
    path('f_delete/<int:f_board_id>/', views.f_delete,name='f_delete'),
    path('download/', views.f_download, name='f_download'),     
     
    
]
