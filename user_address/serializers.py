from rest_framework import serializers
from user_address.models import UserAddressModel

class UserAddressSerializer (serializers.ModelSerializer):
    class Meta:
        model=UserAddressModel
        fields = '__all__'