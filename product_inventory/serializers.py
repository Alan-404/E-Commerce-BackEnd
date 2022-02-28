from rest_framework import serializers
from product_inventory.models import ProductInventoryModel

class ProductInventorySerializer (serializers.ModelSerializer):
    class Meta:
        model = ProductInventoryModel
        fields = '__all__'