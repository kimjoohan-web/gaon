from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'board'
urlpatterns =[
    # path('login/', auth_views.LoginView.as_view(template_name='common/login.html'), name='login'),
    # path('logout/', views.logout_view,name='logout'),
    # path('signup/', views.signup,name='signup'),
    # path('forgot_password/', views.forgot_password,name='forgot_password'), 
    path('<int:category_id>/b_create/', views.b_create,name='b_create'), 
    path('<int:category_id>/', views.b_list,name='b_list'),     
    path('<int:category_id>/<int:qboard_id>/', views.b_detail,name='b_detail'),    
    path('<int:category_id>/b_modify/<int:qboard_id>/', views.b_modify,name='b_modify'),    
    path('<int:category_id>/b_delete/<int:qboard_id>/', views.b_delete,name='b_delete'),
    path('download/', views.file_download, name='file_download'),
    
    # path('question/<int:category_id>/create/',question_views.question_create, name='question_create'),
    # path('question/<int:category_id>/modify/<int:question_id>/',question_views.question_modify, name='question_modify'),
    # path('question/<int:category_id>/delete/<int:question_id>/',question_views.question_delete, name='question_delete'),    
    # path('question/<int:category_id>/vote/<int:question_id>/', question_views.question_vote, name='question_vote'),
    # path('question/<int:category_id>/comment/<int:question_id>/', question_views.question_comment, name='question_comment'),
    
]
