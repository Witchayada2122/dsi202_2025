import os
from pathlib import Path
from dotenv import load_dotenv

# กำหนด Path หลักของโปรเจค
BASE_DIR = Path(__file__).resolve().parent.parent

# โหลดไฟล์ .env
load_dotenv(dotenv_path=BASE_DIR / '.env')

# ความลับของโปรเจค อ่านจาก environment variables
SECRET_KEY = os.getenv('SECRET_KEY')

# เปิดโหมด debug สำหรับพัฒนา (ปิดใน production)
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# แอปพลิเคชันที่ติดตั้ง
INSTALLED_APPS = [
    # แอปพื้นฐานของ Django
    'django.contrib.sites',  # จำเป็นสำหรับ django-allauth
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # แอปของ django-allauth สำหรับระบบล็อกอินและ social account
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

    # แอปของคุณ เช่น clothing
    'clothing',
]

# รายการ middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# กำหนดชื่อไฟล์ URL config หลัก (ตรวจสอบให้ตรงกับชื่อโฟลเดอร์โปรเจคของคุณ)
ROOT_URLCONF = 'rental_shop.urls'  # เปลี่ยนเป็น 'mindvibe.urls' ถ้าโฟลเดอร์โปรเจคชื่อ mindvibe

# ตั้งค่า template engine
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,  # ค้นหา template ในแอปอัตโนมัติ
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',  # จำเป็นสำหรับ allauth
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# กำหนดไฟล์ wsgi สำหรับ deploy
WSGI_APPLICATION = 'rental_shop.wsgi.application'  # เปลี่ยนถ้าโฟลเดอร์โปรเจคไม่ใช่ rental_shop

# ตั้งค่าฐานข้อมูล SQLite (เปลี่ยนตามความเหมาะสม)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ตัวตรวจสอบรหัสผ่าน
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# การตั้งค่าภาษาและ timezone
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Bangkok'
USE_I18N = True
USE_TZ = True

# การตั้งค่าไฟล์ static และ media
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ตั้งค่า URL สำหรับระบบล็อกอินและหลัง logout
LOGIN_URL = 'account_login'  # ชื่อ URL pattern ของ allauth login
LOGIN_REDIRECT_URL = '/'      # หลัง login สำเร็จ
ACCOUNT_LOGOUT_REDIRECT_URL = '/'  # หลัง logout

# ตั้งค่า SITE_ID จำเป็นสำหรับ django-allauth
SITE_ID = 3

# กำหนด Authentication backends
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',          # Default backend ของ Django
    'allauth.account.auth_backends.AuthenticationBackend',  # backend ของ allauth
]

# ตั้งค่า default primary key field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ตั้งค่า social account provider โดยใช้ค่า client_id และ secret จาก environment variables
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': os.getenv('GOOGLE_CLIENT_ID'),
            'secret': os.getenv('GOOGLE_SECRET'),
            'key': ''
        }
    }
}
