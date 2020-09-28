from django.contrib import admin

from .models import *


# Register your models here.

class AuctionItemAdmin(admin.ModelAdmin):
    list_display = ('name','description','image','status', 'owner')

class BidAdmin(admin.ModelAdmin):
    list_display = ('item','value', 'buyer', 'date')


admin.site.register(User)
admin.site.register(Category)
admin.site.register(Comments)
admin.site.register(AuctionItem, AuctionItemAdmin)
admin.site.register(Bid, BidAdmin)
