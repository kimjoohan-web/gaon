from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'vaca'
urlpatterns =[    
    path('', views.index,name='index'),        
    path('leave_request/',views.leave_request, name='leave_request'),  
    path('leave_detail/<int:request_id>/', views.leave_detail, name='leave_detail'),
  
    
]