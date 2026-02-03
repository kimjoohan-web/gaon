from django.urls import path

from . import views
app_name = 'gchat'
urlpatterns = [
    path('', views.index, name='index'),
    path('<str:room_name>/', views.room, name='room'),
    path('<str:room_name>/messages/', views.MessageListView.as_view(), name='message_list'),
    
]