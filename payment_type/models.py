from django.db import models

# Create your models here.

class PaymentTypeModel (models.Model):
    id = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=50)
    description = models.TextField()
    class Meta:
        db_table = 'payment_type'