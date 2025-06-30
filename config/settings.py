import os
from dotenv import load_dotenv
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-i21pn3-fz(zs*z#@@d_l(7qg$8l)xg#ot5ri9i1*en%6$c#+qb'


# SECURITY WARNING: don't run with debug turned on in production!
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
    'dbapp',
    'users',
    'books',
]

# Here apps needing migrations are listed.

CUSTOM_APPS = [
    'dbapp',
    'users',
    'books',
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

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'config', 'templates'),
            os.path.join(BASE_DIR, 'books', 'templates'),
        ],
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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases


load_dotenv()
USER = os.getenv('MS_SQL_USER')
PASSWORD = os.getenv('MS_SQL_KEY')
HOST = os.getenv('MS_SQL_SERVER')
DATABASE = os.getenv('MS_SQL_DATABASE')
DRIVER = os.getenv('MS_SQL_DRIVER')
PAD_DATABASE = os.getenv('MS_PAD_DATABASE')

DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME' : DATABASE,
        'PASSWORD' : PASSWORD,
        'HOST' : HOST,
        'PORT' : '',
        'OPTIONS' : {
            'driver' : DRIVER,
            'extra_params' : f'server={HOST}'
        }
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Yekaterinburg'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

STATICFILES_DIRS = (
    BASE_DIR / 'static',
)

MEDIA_URL = '/media/'

MEDIA_ROOT = (
    BASE_DIR / 'media'
)

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'users.User'

LOGIN_REDIRECT_URL = 'books:books_list'

# Project specific contastants

# Folder used to store books repository files before they are put into the database;
# shoud get deleted after.

TEMP_FOLDER = (
    BASE_DIR / 'temp_files'
)

# GitHub repository from where the books are sourced.

BOOKS_REPO = 'https://github.com/PerseusDL/canonical-latinLit.git'

# Path to book data inside the cloned repository.

REPO_DATA_DIR = (
    TEMP_FOLDER / 'data'
)

# Is necessary for generating urn cts ids which are used in Scaife viewer and Philologic.
# This one should work for most books in the given repository, but must be change for another one.

CTS_URN_PREFIX = 'urn:cts:latinLit:'

# Match languages and the part of book file names that is responsible for language.
# Important for determining language of a book based on file name and for filtering by languages in list views.

LANG_VALUES = {
    'lat': 'latin',
    'eng': 'english',
}

# Tei Garage web hosting adress: https://teigarage.tei-c.org/
# unless hosted locally. 
# Their API is used for converting documents to HTML

TEIGARAGE = 'http://localhost:32768'
