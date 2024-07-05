from django.urls import path
from accounts import views

urlpatterns = [
    path('', views.user_login, name="accounts_default"),
    path('login/', views.user_login, name="user_login"),
    path('logout/', views.user_logout, name="user_logout"),
    path('register/', views.user_register, name="user_register"),
    path('checkusername/', views.check_username, name="user_checkusername"),
    path('password_reset/', views.user_forget, name="user_forget"),
    path('password_change/', views.user_forget, name="change_password"),
    path('edit/', views.user_edit, name="user_edit"),
    path('notifications/', views.user_forget, name="user_notifications"),
    path('follow/', views.user_follow, name="user_follow"),
]
