from django.db import models

# Create your models here.

class DiscountModel (models.Model):
    id = models.AutoField(primary_key=True)
    product_id = models.IntegerField(unique=True, null=False)
    discount_percent = models.FloatField()
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField()
    class Meta:
        db_table = 'discount'

