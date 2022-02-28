from rest_framework import serializers
from cart.models import CartModel

class CartSerializer (serializers.ModelSerializer):
    class Meta:
        model = CartModel
        fields = '__all__'