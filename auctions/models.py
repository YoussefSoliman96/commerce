from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    title = models.CharField(max_length=60)
    
    def __str__(self):
        return self.title

class AuctionListing(models.Model):
    title = models.CharField(max_length=60)
    price = models.FloatField()
    description = models.CharField(max_length=600)
    year = models.FloatField(default="2000")
    imageUrl = models.CharField(max_length=600)
    active = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category", null=True, default=True)

    def __str__(self):
        return self.title