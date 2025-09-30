import requests
import json
from urllib.parse import unquote
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import StockSymbol, StockData, UserWatchlist

def stock_list(request):
    """주식 목록 페이지"""
    # 미리 정의된 종목들
    predefined_symbols = [
        {'symbol': 'AAPL', 'name': 'Apple Inc.', 'exchange': 'NASDAQ', 'category': '미국주식'},
        {'symbol': 'MSFT', 'name': 'Microsoft Corporation', 'exchange': 'NASDAQ', 'category': '미국주식'},
        {'symbol': 'GOOGL', 'name': 'Alphabet Inc.', 'exchange': 'NASDAQ', 'category': '미국주식'},
        {'symbol': 'TSLA', 'name': 'Tesla Inc.', 'exchange': 'NASDAQ', 'category': '미국주식'},
        {'symbol': 'AMZN', 'name': 'Amazon.com Inc.', 'exchange': 'NASDAQ', 'category': '미국주식'},
        {'symbol': '005930', 'name': '삼성전자', 'exchange': 'KOSPI', 'category': '한국주식'},
        {'symbol': '000660', 'name': 'SK하이닉스', 'exchange': 'KOSPI', 'category': '한국주식'},
        {'symbol': '035420', 'name': 'NAVER', 'exchange': 'KOSPI', 'category': '한국주식'},
        {'symbol': 'BTC/USD', 'name': 'Bitcoin', 'exchange': 'Crypto', 'category': '암호화폐'},
        {'symbol': 'ETH/USD', 'name': 'Ethereum', 'exchange': 'Crypto', 'category': '암호화폐'},
        {'symbol': 'USD/KRW', 'name': 'USD/KRW', 'exchange': 'Forex', 'category': '외환'},
        {'symbol': 'EUR/USD', 'name': 'EUR/USD', 'exchange': 'Forex', 'category': '외환'},
        {'symbol': 'GOLD', 'name': 'Gold', 'exchange': 'Commodity', 'category': '원자재'},
        {'symbol': 'WTI', 'name': 'WTI Oil', 'exchange': 'Commodity', 'category': '원자재'},
        {'symbol': '^TNX', 'name': '10-Year Treasury', 'exchange': 'Bond', 'category': '채권'},
    ]
    
    # 데이터베이스에 종목들이 없으면 미리 정의된 종목들을 추가
    if not StockSymbol.objects.exists():
        for symbol_data in predefined_symbols:
            StockSymbol.objects.get_or_create(
                symbol=symbol_data['symbol'],
                defaults={
                    'name': symbol_data['name'],
                    'exchange': symbol_data['exchange'],
                    'category': symbol_data['category']
                }
            )
    
    categories = StockSymbol.objects.values_list('category', flat=True).distinct()
    symbols_by_category = {}
    
    for category in categories:
        symbols_by_category[category] = StockSymbol.objects.filter(category=category, is_active=True)
    
    context = {
        'categories': categories,
        'symbols_by_category': symbols_by_category,
    }
    
    return render(request, 'stock/stock_list.html', context)

def stock_chart(request, symbol):
    """주식 차트 페이지"""
    # URL에서 받은 심볼을 디코딩하여 처리
    symbol = unquote(symbol)
    try:
        stock_symbol = StockSymbol.objects.get(symbol=symbol)
    except StockSymbol.DoesNotExist:
        messages.error(request, '존재하지 않는 종목입니다.')
        return redirect('stock:stock_list')
    
    context = {
        'stock_symbol': stock_symbol,
    }
    
    return render(request, 'stock/stock_chart.html', context)

def trading_view(request, category):
    """TradingView 차트 페이지"""
    category_mapping = {
        'kospi': {
            'symbol': 'KOSPI',
            'name': '코스피',
            'exchange': 'KRX',
            'interval': '1D'
        },
        'nasdaq': {
            'symbol': 'NDX',
            'name': '나스닥100',
            'exchange': 'NASDAQ',
            'interval': '1D'
        },
        'sp500': {
            'symbol': 'SPX',
            'name': 'S&P500',
            'exchange': 'SPX',
            'interval': '1D'
        },
        'bitcoin': {
            'symbol': 'BTCUSD',
            'name': '비트코인',
            'exchange': 'COINBASE',
            'interval': '1D'
        },
        'dollar': {
            'symbol': 'DXY',
            'name': '달러 인덱스',
            'exchange': 'ICE',
            'interval': '1D'
        },
        'gold': {
            'symbol': 'XAUUSD',
            'name': '골드',
            'exchange': 'OANDA',
            'interval': '1D'
        },
        'oil': {
            'symbol': 'WTIUSD',
            'name': 'WTI 원유',
            'exchange': 'NYMEX',
            'interval': '1D'
        },
        'bond10y': {
            'symbol': 'US10Y',
            'name': '10년 국채',
            'exchange': 'CBOE',
            'interval': '1D'
        },
        'bond2y': {
            'symbol': 'US02Y',
            'name': '2년 국채',
            'exchange': 'CBOE',
            'interval': '1D'
        }
    }
    
    if category not in category_mapping:
        messages.error(request, '존재하지 않는 카테고리입니다.')
        return redirect('stock:stock_list')
    
    chart_info = category_mapping[category]
    
    context = {
        'category': category,
        'chart_info': chart_info,
    }
    
    return render(request, 'stock/trading_view.html', context)

@login_required
def add_to_watchlist(request, symbol_id):
    """관심종목 추가"""
    try:
        symbol = StockSymbol.objects.get(id=symbol_id)
        watchlist, created = UserWatchlist.objects.get_or_create(
            user=request.user,
            symbol=symbol
        )
        
        if created:
            messages.success(request, f'{symbol.name}을(를) 관심종목에 추가했습니다.')
        else:
            messages.info(request, f'{symbol.name}은(는) 이미 관심종목에 있습니다.')
            
    except StockSymbol.DoesNotExist:
        messages.error(request, '존재하지 않는 종목입니다.')
    
    return redirect('stock:stock_list')

@login_required
def remove_from_watchlist(request, symbol_id):
    """관심종목 제거"""
    try:
        symbol = StockSymbol.objects.get(id=symbol_id)
        watchlist = UserWatchlist.objects.get(user=request.user, symbol=symbol)
        watchlist.delete()
        messages.success(request, f'{symbol.name}을(를) 관심종목에서 제거했습니다.')
        
    except (StockSymbol.DoesNotExist, UserWatchlist.DoesNotExist):
        messages.error(request, '존재하지 않는 관심종목입니다.')
    
    return redirect('stock:stock_list')

@login_required
def watchlist(request):
    """관심종목 목록"""
    user_watchlist = UserWatchlist.objects.filter(user=request.user).select_related('symbol')
    
    context = {
        'watchlist': user_watchlist,
    }
    
    return render(request, 'stock/watchlist.html', context)

def get_stock_data(request, symbol):
    """실시간 주식 데이터 조회 API"""
    try:
        # URL에서 받은 심볼을 디코딩하여 처리
        symbol = unquote(symbol)
        # Twelve Data API 호출
        api_key = settings.TWELVE_DATA_API_KEY
        url = f"https://api.twelvedata.com/time_series"
        
        params = {
            'symbol': symbol,
            'interval': '1day',
            'outputsize': 30,
            'apikey': api_key
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            return JsonResponse(data)
        else:
            return JsonResponse({'error': 'API 호출 실패'}, status=400)
            
    except requests.RequestException as e:
        return JsonResponse({'error': f'API 호출 오류: {str(e)}'}, status=500)
    except Exception as e:
        return JsonResponse({'error': f'서버 오류: {str(e)}'}, status=500)