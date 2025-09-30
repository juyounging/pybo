from django.contrib import admin
from .models import StockSymbol, StockData, UserWatchlist

@admin.register(StockSymbol)
class StockSymbolAdmin(admin.ModelAdmin):
    list_display = ['symbol', 'name', 'exchange', 'category', 'is_active', 'created_at']
    list_filter = ['category', 'exchange', 'is_active', 'created_at']
    search_fields = ['symbol', 'name']
    list_editable = ['is_active']
    ordering = ['category', 'symbol']

@admin.register(StockData)
class StockDataAdmin(admin.ModelAdmin):
    list_display = ['symbol', 'datetime', 'open_price', 'high_price', 'low_price', 'close_price', 'volume', 'created_at']
    list_filter = ['symbol', 'datetime', 'created_at']
    search_fields = ['symbol__symbol', 'symbol__name']
    ordering = ['-datetime']
    date_hierarchy = 'datetime'

@admin.register(UserWatchlist)
class UserWatchlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'symbol', 'created_at']
    list_filter = ['created_at', 'symbol__category']
    search_fields = ['user__username', 'symbol__symbol', 'symbol__name']
    ordering = ['-created_at']