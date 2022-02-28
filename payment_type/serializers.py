from rest_framework import serializers
from payment_type.models import PaymentTypeModel

class PaymentTypeSerializer (serializers.ModelSerializer):
    class Meta:
        model = PaymentTypeModel
        fields = '__all__'