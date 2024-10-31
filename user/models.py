from django.db import models

class Costumer(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    last_name = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField(max_length=100, null=True, blank=True, unique=True)
    username = models.CharField(max_length=36, help_text='username must be unique and less than 36 characters', unique=True, blank=False, null=False)
    password = models.CharField(max_length=255, help_text='password must be less than 36 characters', blank=False, null=False)  
    address = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=100, null=False, blank=False, unique=True)
    wallet = models.IntegerField(default= 0, blank=False, null= False)

    def __str__(self) -> str:
        return f"{self.name} {self.last_name}"
    
    