# 주식 차트 프로젝트

## 개요
pybo 커뮤니티 사이트에 Twelve Data API와 TradingView 위젯을 활용한 주식 실시간 차트 기능을 추가한 프로젝트입니다.

## 주요 기능

### 1. 주식 목록
- 다양한 카테고리별 주식 목록 (한국주식, 미국주식, 암호화폐, 외환, 원자재, 채권)
- 각 종목별 차트 보기 및 관심종목 추가 기능

### 2. 실시간 차트
- TradingView 위젯을 활용한 실시간 차트
- 코스피, 나스닥100, S&P500, 비트코인, 달러, 골드, 오일, 10년/2년 채권
- 다양한 기술적 지표 (RSI, MACD, Stochastic, Volume)

### 3. 개별 종목 차트
- Twelve Data API를 통한 실시간 데이터 조회
- TradingView 차트와 실시간 가격 정보 표시
- 관심종목 추가/제거 기능

### 4. 관심종목 관리
- 로그인한 사용자만 사용 가능
- 관심종목 추가/제거 및 목록 관리

## 사용된 기술

### Backend
- Django 5.2.6
- Python requests (API 호출)
- Twelve Data API (실시간 주식 데이터)

### Frontend
- Bootstrap 5 (UI 프레임워크)
- TradingView Widget (차트 라이브러리)
- JavaScript (실시간 데이터 업데이트)

### API
- Twelve Data API Key: fe12b205aa7e4b2b939d487d8770ab4e

## 설치 및 실행

### 1. 의존성 설치
```bash
pip install requests
```

### 2. 데이터베이스 마이그레이션
```bash
python manage.py makemigrations stock
python manage.py migrate
```

### 3. 서버 실행
```bash
python manage.py runserver
```

### 4. 접속
- 메인 페이지: http://127.0.0.1:8000/
- 주식 차트: http://127.0.0.1:8000/stock/
- 관리자 페이지: http://127.0.0.1:8000/admin/

## 프로젝트 구조

```
mysite/
├── stock/                    # 주식 앱
│   ├── models.py            # 주식 데이터 모델
│   ├── views.py             # 뷰 함수
│   ├── urls.py              # URL 설정
│   ├── admin.py             # 관리자 설정
│   └── templatetags/        # 커스텀 템플릿 태그
├── templates/stock/         # 주식 템플릿
│   ├── stock_list.html      # 주식 목록
│   ├── stock_chart.html     # 개별 차트
│   ├── trading_view.html    # TradingView 차트
│   └── watchlist.html       # 관심종목
└── static/style.css         # 스타일시트
```

## 모델 설명

### StockSymbol
- 주식 심볼 정보 (심볼, 이름, 거래소, 카테고리)

### StockData
- 주식 데이터 (OHLCV + 시간)

### UserWatchlist
- 사용자별 관심종목 목록

## 주요 URL

- `/stock/` - 주식 목록
- `/stock/chart/<symbol>/` - 개별 차트
- `/stock/trading/<category>/` - TradingView 차트
- `/stock/watchlist/` - 관심종목
- `/stock/api/data/<symbol>/` - 실시간 데이터 API

## 특징

1. **실시간 데이터**: Twelve Data API를 통한 실시간 주식 데이터 조회
2. **인터랙티브 차트**: TradingView 위젯을 활용한 전문적인 차트 분석
3. **사용자 맞춤**: 관심종목 기능으로 개인화된 투자 도구
4. **반응형 디자인**: 모바일과 데스크톱 모두 지원
5. **카테고리별 구성**: 다양한 자산 클래스별 체계적인 구성

## 향후 개선사항

1. 실시간 알림 기능
2. 포트폴리오 관리 기능
3. 백테스팅 기능
4. 더 많은 기술적 지표 추가
5. 모바일 앱 개발
