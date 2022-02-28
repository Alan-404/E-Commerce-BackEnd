from django.urls import path
from payment_type import views

urlpatterns = [
    path('payment_type_api', views.payment_type_api)
]