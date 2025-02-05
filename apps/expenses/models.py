from django.db import models

from apps.core.models import Currency
from apps.products.models import Product


# Create your models here.
class AdExpense(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ['product', 'date']

    def __str__(self):
        return f"{self.product.sku} - {self.date}"