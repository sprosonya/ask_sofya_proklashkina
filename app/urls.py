from django.urls import path

from app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hot/', views.hot, name='hot'),
    path('question/<int:question_id>', views.question, name='question'),
    path('ask/', views.ask, name='ask'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.log_in, name='login'),
    path('settings/', views.settings, name='settings'),
    path('tag/<str:question_tag>', views.tag, name='tag'),
    path('logout/', views.logout, name="logout")
]