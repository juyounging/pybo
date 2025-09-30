from django.urls import path
from . import views

app_name = 'stock'

urlpatterns = [
    path('', views.stock_list, name='stock_list'),
    path('chart/<path:symbol>/', views.stock_chart, name='stock_chart'),
    path('trading/<str:category>/', views.trading_view, name='trading_view'),
    path('watchlist/add/<int:symbol_id>/', views.add_to_watchlist, name='add_to_watchlist'),
    path('watchlist/remove/<int:symbol_id>/', views.remove_from_watchlist, name='remove_from_watchlist'),
    path('watchlist/', views.watchlist, name='watchlist'),
    path('api/data/<path:symbol>/', views.get_stock_data, name='get_stock_data'),
]
