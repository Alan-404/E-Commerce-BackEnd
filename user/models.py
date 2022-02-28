from django.db import models

# Create your models here.

class UserModel (models.Model):
    id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=100, unique=True, null=False)
    password = models.CharField(max_length=150, null=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    bdate = models.DateField()
    gender = models.CharField(max_length=6)
    telephone = models.CharField(max_length=12)
    country = models.CharField(max_length=50)
    avatar = models.TextField()
    role_id = models.IntegerField()
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField()
    class Meta:
        db_table = 'user'
