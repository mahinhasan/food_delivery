from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    CHOICES = [
        ('owner' : 'Owner'),
        ('employee':'Employee'),
        ('customer':'Customer')
        role = models.CharField(choices = CHOICES,max_length=50,default = 'customer')
    ]

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    owner = models.ForeignKey(User, related_name='res_owner', on_delete=models.CASCADE)
    employees = models.ManyToManyField(User, related_name='res_emp')
