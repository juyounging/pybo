# AWS 배포 가이드

## 📋 배포 준비사항

### 1. 필수 도구 설치
```bash
# AWS CLI 설치
pip install awscli

# EB CLI 설치
pip install awsebcli
```

### 2. AWS 계정 설정
```bash
# AWS 자격 증명 설정
aws configure
```

## 🚀 배포 방법

### 방법 1: AWS Elastic Beanstalk (권장)

#### 1단계: EB 애플리케이션 초기화
```bash
cd /path/to/your/project
eb init --platform python-3.11 --region ap-northeast-2
```

#### 2단계: 환경 생성 및 배포
```bash
# 환경 생성
eb create production

# 또는 기존 환경에 배포
eb deploy
```

#### 3단계: 환경 변수 설정
```bash
# EB CLI를 통한 환경 변수 설정
eb setenv SECRET_KEY="your-secret-key-here"
eb setenv DJANGO_SETTINGS_MODULE="mysite.config.settings.prod"
```

### 방법 2: AWS EC2 + Nginx + Gunicorn

#### 1단계: EC2 인스턴스 생성
- Ubuntu 20.04 LTS AMI 선택
- t3.micro 이상 인스턴스 타입
- 보안 그룹에서 HTTP(80), HTTPS(443), SSH(22) 포트 개방

#### 2단계: 서버 설정
```bash
# 서버 접속
ssh -i your-key.pem ubuntu@your-ec2-ip

# 시스템 업데이트
sudo apt update && sudo apt upgrade -y

# 필수 패키지 설치
sudo apt install python3 python3-pip python3-venv nginx git -y

# 프로젝트 클론
git clone https://github.com/your-username/your-repo.git
cd your-repo

# 가상환경 생성 및 활성화
python3 -m venv venv
source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt
```

#### 3단계: Django 설정
```bash
# 정적 파일 수집
python manage.py collectstatic --noinput

# 데이터베이스 마이그레이션
python manage.py migrate

# 슈퍼유저 생성
python manage.py createsuperuser
```

#### 4단계: Gunicorn 설정
```bash
# Gunicorn 서비스 파일 생성
sudo nano /etc/systemd/system/gunicorn.service
```

Gunicorn 서비스 파일 내용:
```ini
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/your-repo
ExecStart=/home/ubuntu/your-repo/venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/home/ubuntu/your-repo/gunicorn.sock mysite.config.wsgi:application

[Install]
WantedBy=multi-user.target
```

#### 5단계: Nginx 설정
```bash
# Nginx 설정 파일 생성
sudo nano /etc/nginx/sites-available/your-site
```

Nginx 설정 파일 내용:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/ubuntu/your-repo;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/your-repo/gunicorn.sock;
    }
}
```

#### 6단계: 서비스 시작
```bash
# Gunicorn 서비스 시작
sudo systemctl start gunicorn
sudo systemctl enable gunicorn

# Nginx 시작
sudo systemctl start nginx
sudo systemctl enable nginx

# 설정 파일 링크
sudo ln -s /etc/nginx/sites-available/your-site /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

## 🔧 환경 변수 설정

### 필수 환경 변수
```bash
SECRET_KEY=your-django-secret-key
DJANGO_SETTINGS_MODULE=mysite.config.settings.prod
TWELVE_DATA_API_KEY=fe12b205aa7e4b2b939d487d8770ab4e
```

### 데이터베이스 설정 (RDS 사용 시)
```bash
DB_NAME=your-db-name
DB_USER=your-db-user
DB_PASSWORD=your-db-password
DB_HOST=your-rds-endpoint
DB_PORT=5432
```

## 📁 파일 구조
```
your-project/
├── mysite/
│   ├── config/
│   │   ├── settings/
│   │   │   ├── base.py
│   │   │   ├── local.py
│   │   │   └── prod.py
│   │   ├── wsgi.py
│   │   └── urls.py
│   ├── pybo/
│   ├── stock/
│   └── manage.py
├── .ebextensions/
│   ├── django.config
│   ├── 01_packages.config
│   └── 02_python.config
├── requirements.txt
├── Procfile
├── runtime.txt
└── .gitignore
```

## 🔍 배포 후 확인사항

### 1. 애플리케이션 상태 확인
```bash
# EB CLI로 로그 확인
eb logs

# 또는 EC2에서 직접 확인
sudo journalctl -u gunicorn
sudo journalctl -u nginx
```

### 2. 정적 파일 서빙 확인
- `/static/` URL로 CSS, JS 파일 접근 가능한지 확인
- 브라우저 개발자 도구에서 404 오류 없는지 확인

### 3. 데이터베이스 연결 확인
- Django 관리자 페이지 접근 가능한지 확인
- 주식 데이터 API 호출 정상 작동하는지 확인

## 🛠️ 문제 해결

### 일반적인 문제들

#### 1. 정적 파일 404 오류
```bash
# 정적 파일 수집
python manage.py collectstatic --noinput

# Nginx 설정 확인
sudo nginx -t
```

#### 2. 데이터베이스 연결 오류
```bash
# 데이터베이스 마이그레이션
python manage.py migrate

# 데이터베이스 상태 확인
python manage.py dbshell
```

#### 3. Twelve Data API 오류
- API 키가 올바른지 확인
- API 호출 제한 확인
- 네트워크 연결 상태 확인

## 📞 지원

배포 과정에서 문제가 발생하면:
1. 로그 파일 확인
2. Django 설정 확인
3. 서버 리소스 사용량 확인
4. 네트워크 연결 상태 확인

## 🔒 보안 고려사항

1. **시크릿 키 관리**: 환경 변수로 관리
2. **HTTPS 설정**: Let's Encrypt 또는 AWS Certificate Manager 사용
3. **방화벽 설정**: 필요한 포트만 개방
4. **정기 업데이트**: 시스템 및 패키지 정기 업데이트
5. **백업**: 데이터베이스 및 파일 정기 백업
