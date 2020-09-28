from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Max
from .forms import ItemForm, BidForm, CommentForm
from .models import User, AuctionItem, Bid, Comments, Category
from decimal import Decimal
from django.contrib.auth.decorators import login_required



def index(request):
    active_items = AuctionItem.objects.filter(status=True)
    categories = Category.objects.all()
    return render(request, "auctions/index.html", {
        'items' : active_items,
        'categories' : categories
    })

def category_view(request, category_name):
    category = Category.objects.get(name=category_name)
    active_items = AuctionItem.objects.filter(status=True, category=category)
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
                'message': "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                'message': "Username already taken."
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
        initial_price = request.POST['current_price']

        #create item
        item = AuctionItem(name=name, description=description,image=image_url, status=True, current_price=initial_price)
        #making the relations
        item.owner = user
        item.category = Category.objects.get(pk=category_id)

        item.save()

        return HttpResponseRedirect(reverse("index"))
    else:
        #validate if the user is logged in
        if request.user.is_authenticated:
            return render(request, "auctions/create.html", {
                'form' : ItemForm(),
            })
        else:
            return render(request, "auctions/login.html", {
                'message': "Login for create a listing."
            })

def item_view(request, item_name):
    if request.method == "GET":
        item = AuctionItem.objects.get(name=item_name)

        #get the current highest bid for the items
        current_bid = Bid.objects.filter(item=item).order_by('-value').first()

        watchlist_users = item.watchlist.all()

        #this is the variable that checks if the item is in the watchlist of the user
        if request.user in watchlist_users:
            watchlist_validation = False
        else:
            watchlist_validation = True

        #this gets all the comments in the item
        comments = Comments.objects.filter(item=item)

        return render(request, "auctions/item.html", {
            'item' : item,
            'bid' : current_bid,
            'watchlist_validation' : watchlist_validation,
            'comments' : comments
        })

@login_required(login_url='login')
def add_watchlist(request, item_id):
    if request.method == "POST":
        item = AuctionItem.objects.get(pk=item_id)
        user = User.objects.filter(username=request.user.username)

        item.watchlist.set(user)
        #item.save()

        return HttpResponseRedirect(reverse("item", args=[item.name]))

@login_required(login_url='login')
def remove_watchlist(request, item_id):
    if request.method == "POST":
        item = AuctionItem.objects.get(pk=item_id)
        user = User.objects.filter(username=request.user.username)

        request.user.watchlist.remove(item)

        return HttpResponseRedirect(reverse("item", args=[item.name]))

@login_required(login_url='login')
def watchlist_view(request):
    watchlist_items = AuctionItem.objects.filter(watchlist=request.user)

    return render(request, "auctions/mywatchlist.html", {
        'items' : watchlist_items
    })

def close_auction(request, item_id):
    if request.method == "POST":
        item = AuctionItem.objects.get(id=item_id)
        item.status = False
        item.save()

        return HttpResponseRedirect(reverse("item", args=[item.name]))

@login_required(login_url='login')
def make_bid(request, item_id):
    if request.method == "POST":
        bid_value = Decimal(request.POST['value'])
        item = AuctionItem.objects.get(pk=item_id)

        if Bid.objects.filter(item=item).exists(): #if already exists a bid on that item
            current_bid = Bid.objects.filter(item=item).order_by('-value').first()
            if bid_value > current_bid.value:
                new_bid = Bid(value=bid_value, item=item, buyer=request.user)
                item.current_price = bid_value
                item.save()
                new_bid.save()
                return HttpResponseRedirect(reverse("item", args=[item.name]))
            else:
                return render(request, "auctions/makebid.html", {
                    'item' : item,
                    'message': "Your bid must be higher than the current one.",
                    'bid_form' : BidForm()
                })
        else:
            #no one has bid on this item yet, so the value can be equal to the initial price
            if bid_value >= item.current_price:
                new_bid = Bid(value=bid_value, item=item, buyer=request.user)
                item.current_price = bid_value
                item.save()
                new_bid.save()
                return HttpResponseRedirect(reverse("item", args=[item.name]))
            else:
                return render(request, "auctions/makebid.html", {
                    "item" : item,
                    "message": "Your bid must be higher than the current one.",
                    'bid_form' : BidForm()
                })
    else:
        item = AuctionItem.objects.get(pk=item_id)
        return render(request, "auctions/makebid.html", {
            'item' : item,
            'bid_form' : BidForm()
        })

@login_required(login_url='login')
def comment(request, item_id):
    if request.method == "POST":
        user = request.user
        item = AuctionItem.objects.get(pk=item_id)
        title = request.POST['title']
        content = request.POST['content']

        new_comment = Comments(title=title, content=content, user=request.user)
        new_comment.item = item
        new_comment.save()

        return HttpResponseRedirect(reverse("item", args=[item.name]))
    else:
        item = AuctionItem.objects.get(pk=item_id)
        return render(request, "auctions/comment.html", {
            'item' : item,
            'form' : CommentForm()
        })
