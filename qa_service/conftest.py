import os
import django
from django.conf import settings

def pytest_configure():
    """Настройка Django для pytest"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qa_service.settings')
    django.setup()
