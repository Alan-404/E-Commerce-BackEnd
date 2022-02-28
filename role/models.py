from django.db import models

# Create your models here.

class RoleModel (models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=False, unique=True)
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField()
    class Meta:
        db_table = 'role'
