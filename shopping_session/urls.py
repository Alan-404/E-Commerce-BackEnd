from django.urls import path
from shopping_session import views
urlpatterns = [
    path('shopping_session_api', views.shopping_session_api)
]