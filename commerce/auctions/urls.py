from django.urls import path
from .models import AuctionItem
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_view, name="create"),
    path("item/<str:item_name>", views.item_view, name="item"),
    path("add/<int:item_id>", views.add_watchlist, name="add_watchlist"),
    path("remove/<int:item_id>", views.remove_watchlist, name="remove_watchlist"),
    path("mywatchlist", views.watchlist_view, name="mywatchlist"),
    path("bid/<int:item_id>", views.make_bid, name="make_bid"),
    path("category/<str:category_name>", views.category_view, name="category"),
    path("close/<int:item_id>", views.close_auction, name="close_auction"),
    path("comment/<int:item_id>", views.comment, name="comment"),


]
