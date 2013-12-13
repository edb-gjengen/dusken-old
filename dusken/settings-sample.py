"""
Django settings for dusken project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'v_-cub3st=0x3h-fafpz*+jqg+ug78jq7se8xn0&s^b9!8j6t_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)
INSTALLED_APPS += (
    'corsheaders',
    'django_extensions',
    'provider',
    'provider.oauth2',
    'south',
    'tastypie',
    # Our app
    'dusken',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
)

ROOT_URLCONF = 'dusken.urls'

WSGI_APPLICATION = 'dusken.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        # Example PostgreSQL config:
        #'ENGINE': 'django.db.backends.postgresql_psycopg2',
        #'NAME': 'dusken_test',
        #'USER': 'postgres',
        #'PASSWORD': '',
        #'HOST': '127.0.0.1',
        #'PORT': '',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Oslo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

# Our own User class used for authentication.
AUTH_USER_MODEL = 'dusken.Member'

TASTYPIE_DEFAULT_FORMATS = ['json']

CORS_ORIGIN_ALLOW_ALL = True
# Allow Ajax calls only from tuple of domain:port
#CORS_ORIGIN_WHITELIST = (
#    '127.0.0.1:3000',
#    'dusken.neuf.no:3000',
#    'dusken.neuf.no',
#)
