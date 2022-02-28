from django.urls import path
from cart import views
urlpatterns = [
    path('cart_api', views.cart_api),
    path('info_cart', views.get_info_cart)
]