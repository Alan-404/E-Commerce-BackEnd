from django.urls import path
from user import views

urlpatterns = [
    path('user_api', views.user_api),
    path('auth_user', views.auth_user),
    path('login_google', views.login_google),
    path('profile', views.get_profile)
]