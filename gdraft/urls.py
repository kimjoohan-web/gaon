from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'gdraft'
urlpatterns =[    
    path('', views.index,name='index'),        
    path('gdraft_submit/',views.gdraft_submit, name='gdraft_submit'),
    path('gdraft_detail/<int:dr_idx>/',views.gdraft_detail, name='gdraft_detail'),
    path('download/', views.download, name='download'),
    path('gdraft_modify/<int:dr_idx>/',views.gdraft_modify, name='gdraft_modify'),
    path('gdraft_delete/<int:dr_idx>/',views.gdraft_delete, name='gdraft_delete'),
    path('gdraft_status/',views.gdraft_status, name='gdraft_status'),
    path('gstatus_submit/',views.gstatus_submit, name='gstatus_submit'),
    path('gdraft_print/<int:dr_idx>/',views.gdraft_print, name='gdraft_print'),
  
    
]