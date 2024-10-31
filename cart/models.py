from django.db import models
from user.models import Costumer
from product.models import Product

class Cart(models.Model):
    code = models.CharField(max_length=16, help_text='cart must be unique and less than 10 characters', unique=True, null=False, blank=False)
    products = models.ManyToManyField(Product, blank=True)
    costumer = models.ForeignKey(Costumer, on_delete=models.CASCADE)
    is_finalized = models.BooleanField(default=False)
    def __str__(self) -> str:
        return f"{self.code} {self.costumer} isfinalized = {self.is_finalized}"
    