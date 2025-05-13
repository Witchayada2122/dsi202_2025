# settings.py

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

SECRET_KEY = 'django-insecure-+i(ay40(up!g-7!uhe%lzma6xoa(4ncwkp8jd%j7b0b4=9&+jn'

DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'clothing',  # แอป clothing ของคุณ
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'rental_shop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # ใช้การค้นหาจากโฟลเดอร์ภายในแอป
        'APP_DIRS': True,  # กำหนดให้ค้นหาจาก app directories
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'rental_shop.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
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

# Internationalization
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# ตั้งค่า URL สำหรับการเข้าถึงไฟล์ static
STATIC_URL = '/static/'
# settings.py

STATIC_URL = '/static/'

# เพิ่ม STATICFILES_DIRS เพื่อบอก Django ว่าให้ดูไฟล์ static จากที่ไหน
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),  # พูดถึงโฟลเดอร์ 'static' ที่อยู่ในระดับโปรเจกต์
]

# กำหนดที่เก็บไฟล์ static ของโปรเจกต์
STATICFILES_DIRS = [
    BASE_DIR / 'static',  # ควรตั้งให้ `static` อยู่ในโปรเจกต์นี้
]

LOGIN_URL = 'clothing:login' # ชื่อ URL pattern ของหน้า login ของคุณ
                            # (ถ้าไม่ได้ใช้ app_name 'clothing' ใน include ก็จะเป็น 'login')
LOGIN_REDIRECT_URL = 'clothing:clothing_list' # หน้าที่ให้ redirect ไปหลัง login สำเร็จ (ถ้าไม่ได้ระบุ next)

# การเก็บไฟล์ static เมื่อใช้คำสั่ง collectstatic สำหรับ production
STATIC_ROOT = BASE_DIR / 'staticfiles'

# ตั้งค่าพื้นที่จัดเก็บไฟล์สื่อ (media files)
MEDIA_URL = '/media/'  # URL ที่จะใช้ในการเข้าถึงไฟล์สื่อ
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # เส้นทางที่เก็บไฟล์ในเครื่อง


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
