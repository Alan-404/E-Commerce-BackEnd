from rest_framework import serializers
from distributor.models import DistributorModel

class DistributorSerializer (serializers.ModelSerializer):
    class Meta:
        model = DistributorModel
        fields = '__all__'