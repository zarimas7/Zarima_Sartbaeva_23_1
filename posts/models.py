from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=55)

class Product(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    photo = models.ImageField(blank=True, null=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_date = models.DateField(auto_now=True)
    modified_date = models.DateField(auto_now_add=True)
    price = models.FloatField()
    categories = models.ManyToManyField(Category)

class Review (models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, related_name="reviews")
    text = models.TextField()
    created_date = models.DateField(auto_now=True)
