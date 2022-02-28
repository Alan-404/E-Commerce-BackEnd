from django.db import models

# Create your models here.

class OrderDetailModel (models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(unique=True, null=False)
    total = models.FloatField()
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField()
    class Meta:
        db_table = 'order_detail'
