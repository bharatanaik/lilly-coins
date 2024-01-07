"settings file - here we have all the constants and configurations"
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-^5qt(g1(%vniv&)5^xwq%c*+eq^rz4hfi27ki%9!)8*qu#=!d*'

DEBUG = True

ALLOWED_HOSTS = ['*']

# SET difficulty - difficulty defines how many zeroes should it contain in prefix
MINING_DIFFICULTY = 3
# How much reward should be given for mining
MINING_REWARD = 50

STARTING_AMOUNT = 100

INSTALLED_APPS = [
    'main',
    'qr_code',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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
ROOT_URLCONF = 'core.urls'

TEMPLATES = [
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

WSGI_APPLICATION = 'core.wsgi.application'

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'ntUltzgEWHpzhHQ9',
        'HOST': 'db.pffnunxtdsxjdnxpisfx.supabase.co',
        'PORT': 5432,
    }
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True
LOGIN_REDIRECT_URL = "account"
LOGOUT_REDIRECT_URL = "/"

AUTH_USER_MODEL = 'main.LillyUser'

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'