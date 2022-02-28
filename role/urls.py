from django.urls import path
from role import views
urlpatterns = [
    path('role_api', views.role_api)
]