from django.urls import path
from category import views
urlpatterns = [
    path('category_api', views.category_api),
    path('get', views.get_category_id)
]