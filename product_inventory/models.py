from django.db import models

# Create your models here.
class ProductInventoryModel (models.Model):
    id = models.AutoField(primary_key=True)
    product_id = models.IntegerField()
    quantity = models.IntegerField()
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField()
    class Meta:
        db_table = 'product_inventory'