# apps/core/models.py
from django.db import models
from django.contrib.auth.models import User

class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True)  # USD, EUR, GBP
    symbol = models.CharField(max_length=1)  # $, €, £
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=4)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code