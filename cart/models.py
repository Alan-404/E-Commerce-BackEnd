from django.db import models
from datetime import datetime

# Create your models here.
class CartModel (models.Model):
    id = models.AutoField(primary_key=True)
    product_id = models.IntegerField(null=False)
    session_id = models.CharField(max_length=50, null=False)
    quantity = models.IntegerField(null=False)
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField()
    class Meta:
        db_table = 'cart'