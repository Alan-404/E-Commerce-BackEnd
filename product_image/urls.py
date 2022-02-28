from django.urls import path
from product_image import views
urlpatterns = [
    path('product_image_api', views.product_image_api),
    path('thumnail', views.active_thumnail),
    path('get_images', views.get_images_product)
]