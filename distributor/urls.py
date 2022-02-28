from django.urls import path
from distributor import views
urlpatterns = [
    path('distributor_api', views.distributor_api),
    path('get_distributor', views.get_distributor)
]