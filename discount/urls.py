from django.urls import path
from discount import views
urlpatterns = [
    path('discount_api', views.discount_api),
    path('get_discount', views.get_discount_of_product)
]