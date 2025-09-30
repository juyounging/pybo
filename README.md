# 📈 Django Stock Chart Application

Django 기반의 실시간 주식 차트 애플리케이션입니다. Twelve Data API와 TradingView 위젯을 활용하여 전 세계 주요 종목의 실시간 데이터와 전문적인 차트 분석을 제공합니다.

## ✨ 주요 기능

### 🏠 **커뮤니티**
- 질문과 답변 게시판
- 사용자 인증 및 권한 관리
- 투표 기능

### 📊 **주식 차트**
- **실시간 차트**: TradingView 위젯을 활용한 전문적인 차트 분석
- **다양한 종목**: 한국주식, 미국주식, 암호화폐, 외환, 원자재, 채권
- **개별 종목 분석**: Twelve Data API를 통한 실시간 데이터 조회
- **관심종목 관리**: 로그인한 사용자만 사용 가능한 개인화된 관심종목 관리

### 🎨 **모던 UI/UX**
- Twelve Data 사이트를 참고한 전문적인 디자인
- 반응형 웹 디자인 (모바일, 태블릿, 데스크톱 지원)
- 부드러운 애니메이션과 호버 효과
- 직관적인 사용자 인터페이스

## 🚀 지원하는 종목들

### 📈 **주요 지수**
- 코스피 (KOSPI)
- 나스닥100 (NASDAQ)
- S&P500

### 💰 **주요 종목**
- **한국주식**: 삼성전자, SK하이닉스, NAVER
- **미국주식**: Apple, Microsoft, Google, Tesla, Amazon
- **암호화폐**: Bitcoin, Ethereum
- **외환**: USD/KRW, EUR/USD
- **원자재**: Gold, WTI Oil
- **채권**: 10년/2년 국채

## 🛠️ 기술 스택

### Backend
- **Django 5.2.6**: 웹 프레임워크
- **Python 3.11**: 프로그래밍 언어
- **SQLite**: 데이터베이스 (개발), PostgreSQL (운영)
- **Twelve Data API**: 실시간 주식 데이터
- **Gunicorn**: WSGI 서버

### Frontend
- **Bootstrap 5**: UI 프레임워크
- **TradingView Widget**: 차트 라이브러리
- **Font Awesome**: 아이콘
- **JavaScript**: 실시간 데이터 업데이트

### Deployment
- **AWS Elastic Beanstalk**: 클라우드 배포
- **AWS EC2**: 가상 서버
- **Nginx**: 웹 서버
- **Git**: 버전 관리

## 📦 설치 및 실행

### 1. 저장소 클론
```bash
git clone https://github.com/your-username/django-stock-chart.git
cd django-stock-chart
```

### 2. 가상환경 생성 및 활성화
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. 의존성 설치
```bash
pip install -r requirements.txt
```

### 4. 환경 변수 설정
```bash
# .env 파일 생성
SECRET_KEY=your-django-secret-key
TWELVE_DATA_API_KEY=fe12b205aa7e4b2b939d487d8770ab4e
```

### 5. 데이터베이스 마이그레이션
```bash
cd mysite
python manage.py makemigrations
python manage.py migrate
```

### 6. 슈퍼유저 생성
```bash
python manage.py createsuperuser
```

### 7. 서버 실행
```bash
python manage.py runserver
```

## 🌐 접속 URL

- **메인 페이지**: http://127.0.0.1:8000/
- **주식 차트**: http://127.0.0.1:8000/stock/
- **관심종목**: http://127.0.0.1:8000/stock/watchlist/
- **관리자 페이지**: http://127.0.0.1:8000/admin/

## 🚀 AWS 배포

자세한 배포 가이드는 [DEPLOYMENT.md](DEPLOYMENT.md)를 참조하세요.

### 빠른 배포 (Elastic Beanstalk)
```bash
# EB CLI 설치
pip install awsebcli

# 초기화 및 배포
eb init --platform python-3.11 --region ap-northeast-2
eb create production
eb deploy
```

## 📁 프로젝트 구조

```
django-stock-chart/
├── mysite/                    # 메인 Django 프로젝트
│   ├── config/               # 프로젝트 설정
│   │   ├── settings/         # 환경별 설정
│   │   │   ├── base.py       # 기본 설정
│   │   │   ├── local.py      # 로컬 개발 설정
│   │   │   └── prod.py       # 운영 환경 설정
│   │   └── wsgi.py          # WSGI 설정
│   ├── pybo/                # 커뮤니티 앱
│   ├── stock/               # 주식 차트 앱
│   │   ├── models.py        # 데이터 모델
│   │   ├── views.py         # 뷰 함수
│   │   ├── urls.py          # URL 설정
│   │   └── templates/       # 템플릿
│   ├── templates/           # 공통 템플릿
│   └── static/              # 정적 파일
├── .ebextensions/           # AWS Elastic Beanstalk 설정
├── requirements.txt         # Python 의존성
├── Procfile                 # 프로세스 정의
├── runtime.txt              # Python 버전
└── DEPLOYMENT.md            # 배포 가이드
```

## 🔧 환경 변수

### 필수 환경 변수
```bash
SECRET_KEY=your-django-secret-key
TWELVE_DATA_API_KEY=your-twelve-data-api-key
DJANGO_SETTINGS_MODULE=mysite.config.settings.prod
```

### 데이터베이스 설정 (RDS 사용 시)
```bash
DB_NAME=your-db-name
DB_USER=your-db-user
DB_PASSWORD=your-db-password
DB_HOST=your-rds-endpoint
DB_PORT=5432
```

## 📊 API 정보

### Twelve Data API
- **API Key**: fe12b205aa7e4b2b939d487d8770ab4e
- **엔드포인트**: https://api.twelvedata.com/time_series
- **용도**: 실시간 주식 데이터 조회

### TradingView Widget
- **라이브러리**: TradingView Charting Library
- **용도**: 전문적인 차트 분석

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.

## 📞 연락처

프로젝트에 대한 질문이나 제안사항이 있으시면 언제든지 연락해 주세요.

## 🙏 감사의 말

- [Django](https://www.djangoproject.com/) - 웹 프레임워크
- [Twelve Data](https://twelvedata.com/) - 실시간 주식 데이터 API
- [TradingView](https://www.tradingview.com/) - 차트 라이브러리
- [Bootstrap](https://getbootstrap.com/) - UI 프레임워크
- [Font Awesome](https://fontawesome.com/) - 아이콘

---

⭐ 이 프로젝트가 도움이 되었다면 Star를 눌러주세요!
