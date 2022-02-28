from rest_framework import serializers
from product_image.models import ProductImageModel
class ProductImageSerializer (serializers.ModelSerializer):
    class Meta:
        model = ProductImageModel
        fields = '__all__'