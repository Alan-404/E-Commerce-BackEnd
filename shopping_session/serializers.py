from rest_framework import serializers
from shopping_session.models import ShoppingSessionModel

class ShoppingSessionSerializer (serializers.ModelSerializer):
    class Meta:
        model = ShoppingSessionModel
        fields = '__all__'