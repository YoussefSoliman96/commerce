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
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category", null=True, default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    watchlist = models.ManyToManyField(User, blank=True, related_name="userWatchlist")

    def __str__(self):
        return self.title