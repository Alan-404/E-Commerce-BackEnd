from django.db import models

# Create your models here.

class DistributorModel (models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150,null=False)
    user_id = models.IntegerField(null=False)
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField()
    class Meta:
        db_table = 'distributor'
