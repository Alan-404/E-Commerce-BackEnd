from rest_framework import serializers
from order_detail.models import OrderDetailModel


class OrderDetailSerializer (serializers.ModelSerializer):
    class Meta:
        model = OrderDetailModel
        fields = '__all__'