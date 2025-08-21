from django.urls import path
from .views import base_views, question_views, answer_views

app_name = 'pybo'
urlpatterns =[
    
    
    path('<int:category_id>/',base_views.list, name='list'),
    path('<int:category_id>/<int:question_id>/',base_views.detail, name='detail'),

    # path('free/',base_views.index, name='index'),
    # path('free/<int:question_id>/',base_views.detail, name='detail'),


    # question_views.py
    path('question/<int:category_id>/create/',question_views.question_create, name='question_create'),
    path('question/<int:category_id>/modify/<int:question_id>/',question_views.question_modify, name='question_modify'),
    path('question/<int:category_id>/delete/<int:question_id>/',question_views.question_delete, name='question_delete'),    
    path('question/<int:category_id>/vote/<int:question_id>/', question_views.question_vote, name='question_vote'),
    path('question/<int:category_id>/comment/<int:question_id>/', question_views.question_comment, name='question_comment'),
  


    # answer_views.py
    path('answer/<int:category_id>/create/<int:question_id>/',answer_views.answer_create, name='answer_create'),
    path('answer/<int:category_id>/modify/<int:answer_id>/',answer_views.answer_modify, name='answer_modify'),
    path('answer/<int:category_id>/delete/<int:answer_id>/',answer_views.answer_delete, name='answer_delete'),
    path('answer/<int:category_id>/vote/<int:answer_id>/',answer_views.answer_vote, name='answer_vote'),
    path('answer/<int:category_id>/comment/<int:answer_id>/',answer_views.answer_comment, name='answer_comment'),


    path('category/', base_views.categoryView, name='categoryView'),

    
    

    

]

