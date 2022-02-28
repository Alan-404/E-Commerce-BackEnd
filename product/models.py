from django.db import models

# Create your models here.

class ProductModel (models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.FloatField()
    sku = models.CharField(max_length=20)
    category_id = models.IntegerField()
    distributor_id = models.IntegerField()
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField()
    class Meta:
        db_table = 'product'