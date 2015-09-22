"""
Django settings for lhcbpr_api project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

# =============================================================================
BASE_DIR = os.path.join(os.path.dirname(__file__), os.pardir)
DB_DIR = os.path.join(BASE_DIR, 'data')
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = os.getenv('DJANGO_STATIC_URL', '/static')
DATA_ROOT = os.path.join(BASE_DIR, 'data')
ROOT_URLCONF = 'urls'

# =============================================================================
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'secret')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DJANGO_DEBUG', True)
TEMPLATE_DEBUG = DEBUG
ALLOWED_HOSTS = []

# =============================================================================
# Application definition
# =============================================================================
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'rest_framework',
    'lhcbpr_api',
    'lhcbpr'  # v1
)
# =============================================================================
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
# =============================================================================
WSGI_APPLICATION = 'wsgi.application'
# =============================================================================
# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
# =============================================================================
DATABASES = {
    'default': {
        'NAME': os.getenv('MYSQL_DATABASE', 'lhcbpr'),
        'USER': os.getenv('MYSQL_USER', ''),
        'PASSWORD': os.getenv('MYSQL_PASSWORD', ''),
        'ENGINE': os.getenv('DJANGO_DB_DEFAULT_ENGINE', 'django.db.backends.mysql'),
        'HOST': os.getenv('DJANGO_DB_HOST', 'lhcbpr-mysql'),
        'PORT': os.getenv('MYSQL_PORT', 3306),
    }
}
# =============================================================================

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/


REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.JSONPRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'PAGINATE_BY': 10,                 # Default to 10
    # Allow client to override, using `?page_size=xxx`.
    'PAGINATE_BY_PARAM': 'page_size',
    # Maximum limit allowed when using `?page_size=xx
    'MAX_PAGINATE_BY': 100
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        }
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
    },
}

ZIP_DIR = DB_DIR
JOBS_UPLOAD_DIR = os.path.join(DATA_ROOT, 'jobs')
