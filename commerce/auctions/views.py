from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Max
from .forms import ItemForm, BidsForm
from .models import User, AuctionItem, Bids, Comments, Category


def index(request):
    active_items = AuctionItem.objects.filter(status=True)
    categories = Category.objects.all()
    return render(request, "auctions/index.html", {
        'items' : active_items,
        'categories' : categories
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def create_view(request):
    if request.method == "POST":
        #getting data from post
        owner = request.user.username
        user = User.objects.get(username=owner)
        name = request.POST['name']
        description = request.POST['description']
        image_url = request.POST['image']
        category_id = request.POST['category']
        value = request.POST['value']

        #create item
        item = AuctionItem(name=name, description=description,image=image_url, status=True, current_price=value)
        #making the relations
        item.owner = user
        item.category = Category.objects.get(pk=category_id)

        item.save()

        #making the first bid made by the owner of the item
        initial_bid = Bids(value=value)
        initial_bid.buyer = user
        initial_bid.item = item
        initial_bid.save()

        return HttpResponseRedirect(reverse("index"))
    else:
        #validate if the user is logged in
        if request.user.is_authenticated:
            return render(request, "auctions/create.html", {
                "form" : ItemForm(),
                "bid_form" : BidsForm()
            })
        else:
            return render(request, "auctions/login.html", {
                "message": "Login for create a listing."
            })

def item_view(request, item_name):
    if request.method == "GET":
        item = AuctionItem.objects.get(name=item_name)

        #get the current highest bid for the items
        current_bid = Bids.objects.filter(item=item).order_by('-value').first()

        watchlist_users = item.watchlist.all()

        if request.user in watchlist_users:
            watchlist_validation = False
        else:
            watchlist_validation = True

        return render(request, "auctions/item.html", {
            'item' : item,
            'bid' : current_bid,
            'watchlist_validation' : watchlist_validation
        })

def add_watchlist(request, item_id):
    if request.method == "POST":
        item = AuctionItem.objects.get(pk=item_id)
        user = User.objects.filter(username=request.user.username)

        item.watchlist.set(user)
        #item.save()

        return HttpResponseRedirect(reverse("item", args=[item.name]))

def remove_watchlist(request, item_id):
    if request.method == "POST":
        item = AuctionItem.objects.get(pk=item_id)
        user = User.objects.filter(username=request.user.username)

        request.user.watchlist.remove(item)

        return HttpResponseRedirect(reverse("item", args=[item.name]))
