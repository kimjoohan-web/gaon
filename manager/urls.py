from django.urls import path
from django.contrib.auth import views as auth_views
# from . import views
from .views import base_views, question_views, answer_views
# , question_views, answer_views
app_name = 'manager'
urlpatterns =[
    path('', base_views.index, name='index'),    
    path('mpybo/<int:category_id>/',base_views.list, name='list'),
    path('mpybo/<int:category_id>/<int:question_id>/',base_views.detail, name='detail'),


    path('mpybo/question/<int:category_id>/create/',question_views.question_create, name='question_create'),
    path('mpybo/question/<int:category_id>/modify/<int:question_id>/',question_views.question_modify, name='question_modify'),
    path('mpybo/question/<int:category_id>/delete/<int:question_id>/',question_views.question_delete, name='question_delete'),    
    path('mpybo/question/<int:category_id>/vote/<int:question_id>/', question_views.question_vote, name='question_vote'),
    path('mpybo/question/<int:category_id>/comment/<int:question_id>/', question_views.question_comment, name='question_comment'),
    
    # answer_views.py
    path('mpybo/<int:category_id>/create/<int:question_id>/',answer_views.answer_create, name='answer_create'),
    path('mpybo/<int:category_id>/modify/<int:answer_id>/',answer_views.answer_modify, name='answer_modify'),
    path('mpybo/<int:category_id>/delete/<int:answer_id>/',answer_views.answer_delete, name='answer_delete'),
    path('mpybo/<int:category_id>/vote/<int:answer_id>/',answer_views.answer_vote, name='answer_vote'),
    path('mpybo/<int:category_id>/comment/<int:answer_id>/',answer_views.answer_comment, name='answer_comment'),

]
