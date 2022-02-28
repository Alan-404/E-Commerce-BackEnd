from django.urls import path
from product import views
urlpatterns = [
    path('product_api', views.product_api),
    path('dashboard', views.get_products_dashboard),
    path('category', views.get_products_category),
    path('get_product', views.get_product_id)
]