from django.db import models
from django.contrib.auth.models import User

class StockSymbol(models.Model):
    """주식 심볼 모델"""
    symbol = models.CharField(max_length=20, unique=True, verbose_name='심볼')
    name = models.CharField(max_length=100, verbose_name='종목명')
    exchange = models.CharField(max_length=50, verbose_name='거래소')
    category = models.CharField(max_length=50, verbose_name='카테고리')
    is_active = models.BooleanField(default=True, verbose_name='활성화')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일시')
    
    class Meta:
        verbose_name = '주식 심볼'
        verbose_name_plural = '주식 심볼들'
        ordering = ['category', 'symbol']
    
    def __str__(self):
        return f"{self.symbol} - {self.name}"

class StockData(models.Model):
    """주식 데이터 모델"""
    symbol = models.ForeignKey(StockSymbol, on_delete=models.CASCADE, verbose_name='심볼')
    datetime = models.DateTimeField(verbose_name='날짜시간')
    open_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='시가')
    high_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='고가')
    low_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='저가')
    close_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='종가')
    volume = models.BigIntegerField(verbose_name='거래량')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일시')
    
    class Meta:
        verbose_name = '주식 데이터'
        verbose_name_plural = '주식 데이터들'
        ordering = ['-datetime']
        unique_together = ['symbol', 'datetime']
    
    def __str__(self):
        return f"{self.symbol.symbol} - {self.datetime}"

class UserWatchlist(models.Model):
    """사용자 관심종목 모델"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='사용자')
    symbol = models.ForeignKey(StockSymbol, on_delete=models.CASCADE, verbose_name='심볼')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일시')
    
    class Meta:
        verbose_name = '관심종목'
        verbose_name_plural = '관심종목들'
        unique_together = ['user', 'symbol']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.symbol.symbol}"