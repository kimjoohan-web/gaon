from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
# from .views import base_views, question_views, answer_views
# , question_views, answer_views
app_name = 'psecu'
urlpatterns =[
    path('',views.index, name='index'),    
    path('psecu_submit/',views.psecu_submit, name='psecu_submit'),
    path('<int:p_wb_idx>/', views.psecu_detail, name='psecu_detail'),
    path('modify/<int:p_wb_idx>/', views.psecu_modify, name='psecu_modify'),
    path('psecu_ch_confirm/', views.psecu_ch_confirm, name='psecu_ch_confirm'),
    path('psecu_review_confirm/', views.psecu_review_confirm, name='psecu_review_confirm'),
  


]
