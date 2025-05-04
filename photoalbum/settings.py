import os
from pathlib import Path
import dj_database_url
from storages.backends.s3boto3 import S3Boto3Storage

BASE_DIR = Path(__file__).resolve().parent.parent

# Adatbázis konfiguráció
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/photoalbum'),
        conn_max_age=600
    )
}

# AWS S3 konfiguráció
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME', 'eu-central-1')
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com'
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

# Statikus fájlok konfigurációja
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'

# Media fájlok konfigurációja
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'

# Debug mód kikapcsolása éles környezetben
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# Biztonsági beállítások
ALLOWED_HOSTS = ['*']  # Éles környezetben pontosítsd ezt!
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False 