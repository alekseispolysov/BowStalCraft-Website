"""
Django settings for bowcraftorg project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import os

from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

from django.contrib.messages import constants as messages

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# Create a new security key to your project and place it in .env file. It will be loaded here
# if secrete key is not created, then default-secret key will be put in place
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'default-secret-key-if-not-found')


# Security
SESSION_COOKIE_HTTPONLY = True

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

CSRF_COOKIE_SECURE = False
CSRF_COOKIE_SAMESITE = 'Lax'  # or 'None' if using cross-site requests

CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8080',  # Add your development URL here
    'http://127.0.0.1:8080',  # You may also want to add this for localhost
    # 'https://yourdomain.com',  # Add your production domain here if applicable
]

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# CKEDITOR_BASEPATH = "/assets/ckeditor"

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # INSTALLED PLUGINS IN PROCESS
    'crispy_bootstrap4', # crispy bootstrap
    'django_ckeditor_5', # new version of django CK Editor
    'corsheaders', # rest framework features
    'rest_framework',
    'crispy_forms', # for crispy forms
    'extra_views', # for formset view generic
    'channels', # for chat(with websockets), channels
    'taggit', # for tags db working
    'django_filters', # filters stuff
    'bootstrapform', # bootstrap styling
    'django_admin_filter', # admin filters automatic
    'captcha', # captcha app


    # PROJECT APPLICATIONS
    'mainapp.apps.MainappConfig',
    'forum.apps.ForumConfig',
    'authentication.apps.AuthenticationConfig',

]



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Insert here
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

# STATIC STORAGE COPY THAT IF IT IS WORKS TO A OLD FILES
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

ROOT_URLCONF = 'bowcraftorg.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries':{
            'forum_extras':'forum.templatetags.forum_extras',
            }
        },
    },
]

WSGI_APPLICATION = 'bowcraftorg.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
# In this project SQLITE3 Database had been used
# This is sqlite3 database, you can change it if you want to use other type of database, for example PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'TEST': {
            'NAME': os.path.join(BASE_DIR, 'db_test.sqlite3')
        }
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = (
os.path.join(BASE_DIR, 'assets'),
)


# crispy forms
CRISPY_TEMPLATE_PACK = 'bootstrap4'
CRISPY_FAIL_SILENTLY = not DEBUG

# login redirect
LOGIN_REDIRECT_URL = 'mainapp:news-page'
LOGOUT_REDIRECT_URL = 'mainapp:news-page'


# try that
LOGIN_URL = 'authentication:login'

# email setup (setup this only, when you want to make password reset feature work. Use env variables to do that)

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'abcd@gmail.com'
EMAIL_HOST_PASSWORD = '123456'


# tagging setting
FORCE_LOWERCASE_TAGS = True



# settings of django-rest framework


CORS_ORIGIN_WHITELIST = [
     'http://localhost:3000'
]


# setting up the messages by django

MESSAGE_TAGS = {
        messages.DEBUG: 'alert-secondary',
        messages.INFO: 'alert-info',
        messages.SUCCESS: 'alert-success',
        messages.WARNING: 'alert-warning',
        messages.ERROR: 'alert-danger',
 }



# captcha output format 
CAPTCHA_OUTPUT_FORMAT = None
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
SILENCED_SYSTEM_CHECKS = ['captcha.recaptcha_test_key_error']


# # ASGI application configuration


ASGI_APPLICATION = 'bowcraftorg.asgi.application'


# path to my login by email backend

AUTHENTICATION_BACKENDS = ('authentication.backends.EmailBackend', 'django.contrib.auth.backends.ModelBackend',)

ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False

# admin filter
ADMIN_FILTER_HISTORY_LIMIT = 3
ADMIN_FILTER_TRUNCATE_HISTORY = True
ADMIN_FILTER_URL_PATH = 'filter/'


# ckeditor5 settings/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')  # Ensure this points to your actual media folder

# Specify the storage class for file uploads
CKEDITOR_5_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

customColorPalette = [
        {
            'color': 'hsl(4, 90%, 58%)',
            'label': 'Red'
        },
        {
            'color': 'hsl(340, 82%, 52%)',
            'label': 'Pink'
        },
        {
            'color': 'hsl(291, 64%, 42%)',
            'label': 'Purple'
        },
        {
            'color': 'hsl(262, 52%, 47%)',
            'label': 'Deep Purple'
        },
        {
            'color': 'hsl(231, 48%, 48%)',
            'label': 'Indigo'
        },
        {
            'color': 'hsl(207, 90%, 54%)',
            'label': 'Blue'
        },
    ]

CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': ['heading', '|', 'bold', 'italic', 'link',
                    'bulletedList', 'numberedList', 'blockQuote', 'imageUpload', ],

    },
    'extends': {
        'blockToolbar': [
            'paragraph', 'heading1', 'heading2', 'heading3',
            '|',
            'bulletedList', 'numberedList',
            '|',
            'blockQuote',
        ],
        'toolbar': ['heading', '|', 'outdent', 'indent', '|', 'bold', 'italic', 'link', 'underline', 'strikethrough',
        'code','subscript', 'superscript', 'highlight', '|', 'codeBlock', 'sourceEditing', 'insertImage',
                    'bulletedList', 'numberedList', 'todoList', '|',  'blockQuote', 'imageUpload', '|',
                    'fontSize', 'fontFamily', 'fontColor', 'fontBackgroundColor', 'mediaEmbed', 'removeFormat',
                    'insertTable',],
        'image': {
            'toolbar': ['imageTextAlternative', '|', 'imageStyle:alignLeft',
                        'imageStyle:alignRight', 'imageStyle:alignCenter', 'imageStyle:side',  '|'],
            'styles': [
                'full',
                'side',
                'alignLeft',
                'alignRight',
                'alignCenter',
            ]

        },
        'table': {
            'contentToolbar': [ 'tableColumn', 'tableRow', 'mergeTableCells',
            'tableProperties', 'tableCellProperties' ],
            'tableProperties': {
                'borderColors': customColorPalette,
                'backgroundColors': customColorPalette
            },
            'tableCellProperties': {
                'borderColors': customColorPalette,
                'backgroundColors': customColorPalette
            }
        },
        'heading' : {
            'options': [
                { 'model': 'paragraph', 'title': 'Paragraph', 'class': 'ck-heading_paragraph' },
                { 'model': 'heading1', 'view': 'h1', 'title': 'Heading 1', 'class': 'ck-heading_heading1' },
                { 'model': 'heading2', 'view': 'h2', 'title': 'Heading 2', 'class': 'ck-heading_heading2' },
                { 'model': 'heading3', 'view': 'h3', 'title': 'Heading 3', 'class': 'ck-heading_heading3' }
            ]
        }
    },
    'list': {
        'properties': {
            'styles': 'true',
            'startIndex': 'true',
            'reversed': 'true',
        }
    }
}

# Define a constant in settings.py to specify file upload permissions
CKEDITOR_5_FILE_UPLOAD_PERMISSION = "authenticated"  # Possible values: "staff", "authenticated", "any"