from django.db import models

# Create your models here.

class Post(models.Model):
    image = models.ImageField(blank=True, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_date = models.DateField(auto_now=True)
    modified_date = models.DateField(auto_now_add= True)
    rate = models.FloatField()

class Product(models.Model):
    photo = models.ImageField(blank=True, null=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_date = models.DateField(auto_now=True)
    modified_date = models.DateField(auto_now_add=True)
    price = models.FloatField()
