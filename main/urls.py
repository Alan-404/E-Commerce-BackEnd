"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('category/', include('category.urls')),
    path('distributor/', include('distributor.urls')),
    path('user_address/',include('user_address.urls')),
    path('role/', include('role.urls')),
    path('product/', include('product.urls')),
    path('product_image/', include('product_image.urls')),
    path('product_inventory/', include('product_inventory.urls')),
    path('discount/', include('discount.urls')),
    path('shopping_session/', include('shopping_session.urls')),
    path('cart/', include('cart.urls')),
    path('payment_type/', include('payment_type.urls')),
    path('banner/', include('banner.urls'))
]
