from django.db import models

# Create your models here.

class CategoryModel (models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=False)
    description = models.TextField()
    thumnail = models.TextField()
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField()
    class Meta:
        db_table = 'category'
