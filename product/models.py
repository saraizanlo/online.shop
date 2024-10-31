from django.db import models
from user.models import Costumer

class Category(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    def __str__(self) -> str:
        return self.name
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    
class Product(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    price = models.DecimalField(max_digits=20, decimal_places=2, blank=False, null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    stock = models.IntegerField(blank=False, null=False)
    def __str__(self) -> str:
        return self.name
    
class Comment(models.Model):
    comment_text = models.TextField(null=False, blank=False)
    costumer = models.ForeignKey(Costumer, on_delete=models.CASCADE,blank=False, null=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,blank=False, null=False)

    def __str__(self) -> str:
        return f"{self.costumer} {self.product}"

class Rate(models.Model):
    rate = models.IntegerField(null=False, blank=False)
    costumer = models.ForeignKey(Costumer, on_delete=models.CASCADE,blank=False, null=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,blank=False, null=False)

    def __str__(self) -> str:
        return f"{self.rate} {self.costumer} {self.product}"
