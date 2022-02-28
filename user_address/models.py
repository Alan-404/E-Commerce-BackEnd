from django.db import models

# Create your models here.

class UserAddressModel(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(null=False)
    address = models.TextField()
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField()
    class Meta:
        db_table = 'user_address'
