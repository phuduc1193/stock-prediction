from django.db import models

# Create your models here.
class StockSector(models.Model):
    class Meta:
        ordering = ['name']
    name = models.CharField(max_length=50)
    slug = models.CharField(max_length=50)

class Company(models.Model):
    class Meta:
        ordering = ['name']

    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True, null=True)
    website = models.CharField(max_length=50)
    ceo = models.CharField(max_length=100)
    sector = models.ForeignKey(StockSector, blank=True, null=True, on_delete=models.CASCADE)

class StockPrice(models.Model):
    class Meta:
        ordering = ['-timestamp']

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    high = models.DecimalField(max_digits=10, decimal_places=2)
    low = models.DecimalField(max_digits=10, decimal_places=2)
    open = models.DecimalField(max_digits=10, decimal_places=2)
    close = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField()