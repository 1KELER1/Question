import os
from pathlib import Path
from decouple import config
from typing import List, Dict, Any

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY: str = config('SECRET_KEY', default='django-insecure-key-for-dev')

DEBUG: bool = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS: List[str] = ['localhost', '127.0.0.1', '0.0.0.0']

INSTALLED_APPS: List[str] = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'qa_api',
]

MIDDLEWARE: List[str] = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF: str = 'qa_service.urls'

TEMPLATES: List[Dict[str, Any]] = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
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

WSGI_APPLICATION: str = 'qa_service.wsgi.application'

DATABASE_URL: str = config('DATABASE_URL', default='postgresql://qa_user:qa_password@localhost:5432/qa_db')

DATABASES: Dict[str, Dict[str, str]] = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DATABASE_URL.split('/')[-1],
        'USER': DATABASE_URL.split('//')[1].split(':')[0],
        'PASSWORD': DATABASE_URL.split('//')[1].split(':')[1].split('@')[0],
        'HOST': DATABASE_URL.split('@')[1].split(':')[0],
        'PORT': DATABASE_URL.split(':')[-1].split('/')[0],
    }
}



REST_FRAMEWORK: Dict[str, Any] = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ]
}

LANGUAGE_CODE: str = 'ru-ru'
TIME_ZONE: str = 'UTC'
USE_I18N: bool = True
USE_TZ: bool = True

STATIC_URL: str = '/static/'
STATIC_ROOT: str = os.path.join(BASE_DIR, 'staticfiles')

DEFAULT_AUTO_FIELD: str = 'django.db.models.BigAutoField'

LOGGING: Dict[str, Any] = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'qa_api': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
