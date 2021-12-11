from django.urls import path
from . import views 
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('', views.home, name='home'),
    path('news/', views.news, name='news'),
    path('register/', views.register, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),
    path('games/', views.games, name='games'),
    path('gamesPage/<str:pk>/', views.gamesPage, name='gamesPage'),
    path('uploadGame/', views.uploadGame, name='uploadGame'),
    path('newsPage/<str:pk>/', views.newsPage, name='newsPage'),
    path('uploadNews/', views.uploadNews, name='uploadNews'),
    path('postComment/', views.comment, name="comment"),
    path('weather/', views.weather, name='weather'),
    path('covid/', views.covid, name='covid'),
    path('gamesapi/', views.gamesapi, name='gamesapi'),
    path('scoreGame/', views.scoreGame, name='scoreGame'),
    path('postCommentGame/', views.commentGame, name="commentGame"),
    path('forum/', views.topics, name='topics'),
    path('topicPage/<str:pk>/', views.topicPage, name='topicPage'),
    path('postCommentTopic/', views.commentTopic, name="commentTopic"),
    path('uploadTopic/', views.uploadTopic, name='uploadTopic'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)