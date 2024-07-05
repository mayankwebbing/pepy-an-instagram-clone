from django.urls import path
from accounts import views

urlpatterns = [
    path('auth/login/', views.user_login, name="user_login"),
    path('auth/logout/', views.user_logout, name="user_logout"),
    path('auth/register/', views.user_register, name="user_register"),
    path('auth/checkusername/', views.check_username, name="user_checkusername"),
    path('auth/forget-password/', views.user_forget, name="user_forget"),
    path('auth/change-password/', views.user_forget, name="change_password"),
    path('edit/', views.user_forget, name="user_settings"),
    path('notifications/', views.user_forget, name="user_settings"),
    path('follow/', views.user_follow, name="user_follow"),
]
