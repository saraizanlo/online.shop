from user.models import Costumer
from product.models import Product
from cart.models import Cart
from django.db import models

class Discount(models.Model):
    code = models.CharField(max_length=16, help_text='code must be unique and less than 10 characters', unique=True, null=False, blank=False)
    percentage = models.IntegerField(null=False, blank=False)
    start_date = models.DateField(null=False, blank=False)
    end_date = models.DateField(null=False, blank=False)
    def __str__(self) -> str:
        return f"{self.code}"
    
class Order(models.Model):
    code = models.CharField(max_length=16, help_text='code must be unique and less than 10 characters', unique=True, null=False, blank=False)
    costumer = models.ForeignKey(Costumer, on_delete=models.CASCADE,blank=False, null=False)
    products = models.ManyToManyField(Product, blank=True)
    discount = models.ForeignKey(Discount, on_delete=models.PROTECT,blank=True, null=True)
    cart = models.OneToOneField(Cart, on_delete=models.PROTECT,blank=False, null=False)
    is_received = models.BooleanField(default=False)
    def __str__(self) -> str:
        return f"{self.code} {self.costumer} is received = {self.is_received}"       