from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

#Category class
class Category(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=128)

    def __str__(self):
        return f"Category {self.id}: {self.name}"

#auction Listings model
class AuctionItem(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    image = models.URLField(blank=True)
    vendor = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=False)
    category = models.ManyToManyField(Category, related_name="categories", blank = True)
    watchlist = models.ManyToManyField(User, related_name="watchlist", blank = True)

    def __str__(self):
        return f"Auction Item ID: {self.id} - Name: {self.name} - Posted by: {self.vendor}"

#Bids model
class Bids(models.Model):
    item = models.ForeignKey(AuctionItem, on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
        return f"Bid of {self.value} on item {self.item.name} - Made by: {self.buyer}"

#Comment model
class Comments(models.Model):
    title = models.CharField(max_length=64)
    content = models.CharField(max_length=256)
    item = models.ForeignKey(AuctionItem, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Comment ID {self.id} on item {self.item.name} - Made by: {self.user.name} on {self.time}"
