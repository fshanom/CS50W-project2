from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator

class User(AbstractUser):
    pass

#Category class
class Category(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=128)

    def __str__(self):
        return self.name

#auction Listings model
class AuctionItem(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    image = models.URLField(blank=True)
    status = models.BooleanField(blank=True)
    date = models.DateTimeField(auto_now_add=True)
    current_price = models.DecimalField(max_digits=10,decimal_places=2, validators=[MinValueValidator(0.01)])

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings", default=None)
    category = models.ForeignKey(Category, on_delete=models.SET(None), null=True,related_name="category")
    watchlist = models.ManyToManyField(User, related_name="watchlist", blank=True)

    def __str__(self):
        return f"Auction Item ID: {self.id} - Name: {self.name}"

#Bids model
class Bids(models.Model):
    item = models.ForeignKey(AuctionItem, on_delete=models.CASCADE, related_name="item")
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    value = models.DecimalField(max_digits=10,decimal_places=2, default=0, validators=[MinValueValidator('0.01')])
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bid of {self.value} on item {self.item.name} - Made by: {self.buyer}"

#Comment model
class Comments(models.Model):
    title = models.CharField(max_length=64)
    content = models.CharField(max_length=256)
    item = models.ForeignKey(AuctionItem, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment ID {self.id} on item {self.item.name} - Made by: {self.user.name} on {self.time}"
