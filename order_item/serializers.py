from rest_framework import serializers
from order_item.models import OrderItemModel

class OrderItemSerializer (serializers.ModelSerializer):
    class Meta:
        model = OrderItemModel
        fields = '__all__'