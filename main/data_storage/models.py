from django.db import models

# Create your models here.
class StockSector(models.Model):
    name = models.CharField(max_length=50)

class Company(models.Model):
    name = models.CharField(max_length=100)
    stock_symbol = models.CharField(max_length=10)
    sector = models.ForeignKey(StockSector, on_delete=models.CASCADE)

class StockPrice(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    high = models.DecimalField(max_digits=10, decimal_places=2)
    low = models.DecimalField(max_digits=10, decimal_places=2)
    open = models.DecimalField(max_digits=10, decimal_places=2)
    close = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField()