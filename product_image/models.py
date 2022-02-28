from django.db import models

# Create your models here.

class ProductImageModel (models.Model):
    id = models.AutoField(primary_key=True)
    product_id = models.IntegerField(null=False)
    image = models.TextField()
    thumnail = models.BooleanField()
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField()
    class Meta:
        db_table = 'product_image'
