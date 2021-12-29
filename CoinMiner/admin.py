# Register your models here.
from django.contrib import admin

from .models import MineAmount, Coin, Account, CoinAmount

class CoinAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['description']}),
        ('Date information', {'fields': ['pub_date']}),
    ]

class AccountAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['miner']}),
        ('ProcessingPower information', {'fields': ['ProcessingPower']}),
    ]

class CoinAmountAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['miner']}),
        ('Coin Information', {'fields': ['coin']}),
        ('Amount information', {'fields': ['amount']}),        
    ]

admin.site.register(MineAmount)
admin.site.register(Coin, CoinAdmin)

admin.site.register(CoinAmount)
admin.site.register(Account, AccountAdmin)