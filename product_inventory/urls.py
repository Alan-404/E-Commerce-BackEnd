from django.urls import path
from product_inventory import views

urlpatterns = [
    path('product_inventory_api', views.product_inventory_api)
]