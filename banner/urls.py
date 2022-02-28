from django.urls import path
from banner import views
urlpatterns = [
    path('banner_api', views.banner_api)
]