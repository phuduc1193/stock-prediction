from django.db import models

# Create your models here.
class StockModel(models.Model):
    symbol = models.CharField(max_length=10)
    model_name = models.CharField(max_length=50)
    scaler_name = models.CharField(max_length=50)
    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)