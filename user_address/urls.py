from django.urls import path
from user_address import views
urlpatterns = [
    path('user_address_api', views.user_address_api),
    path('user_side', views.address_user_side)
]