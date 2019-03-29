from django.db import models

# Create your models here.
class StockModel(models.Model):
    model_location = models.CharField(max_length=100)
    scaler_location = models.CharField(max_length=100)
    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)