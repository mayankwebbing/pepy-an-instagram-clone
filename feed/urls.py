from django.urls import path
from feed import views

urlpatterns = [
    path('', views.home, name="home"),
    path('create-post/', views.create_post, name="create_post"),
    path('post-comment/', views.post_comment, name="post_comment"),
    path('explore/', views.explore, name="explore"),
    path('search/', views.search, name="search"),
    path('notifications/', views.notifications, name="notifications"),
]
