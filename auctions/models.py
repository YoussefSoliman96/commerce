from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    title = models.CharField(max_length=60)
    image = models.CharField(max_length=600)
    
    def __str__(self):
        return self.title

class Bid(models.Model):
    bid = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="bidder")
    

class AuctionListing(models.Model):
    title = models.CharField(max_length=60)
    price = models.ForeignKey(Bid, on_delete=models.CASCADE, blank=True, null=True, related_name="userBid")
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
    
class Comment(models.Model):
    writer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="commentWriter")
    item = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, blank=True, null=True, related_name="itemComments")
    listingComment = models.CharField(max_length=600)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.writer} commented on {self.item}"

