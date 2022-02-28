from rest_framework import serializers
from discount.models import DiscountModel

class DiscountSerializer (serializers.ModelSerializer):
    class Meta:
        model = DiscountModel
        fields = '__all__'