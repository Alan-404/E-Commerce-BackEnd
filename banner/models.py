from django.db import models

# Create your models here.


class BannerModel (models.Model):
    id = models.AutoField(primary_key=True)
    image = models.TextField()
    distributor_id = models.IntegerField()
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField()
    class Meta:
        db_table = 'banner'