from django.db import models

# Create your models here.

class ShoppingSessionModel (models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    user_id = models.IntegerField(null=False, unique=True)
    total = models.FloatField(default=0)
    class Meta:
        db_table = 'shopping_session'

