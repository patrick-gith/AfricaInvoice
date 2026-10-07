import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent
# --- Sécurité ---
SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'django-insecure-change-me-in-production-25@*vtcn+rx8^cia90*sg$89'
)
DEBUG = os.environ.get('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# --- Apps ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    'corsheaders',
    'crispy_forms',
    'crispy_bootstrap5',

    'InvoiceApp',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = 'ProjectInvoice.urls'

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
                'InvoiceApp.context_processors.company_processor',
            ],
            'builtins': [
                'crispy_forms.templatetags.crispy_forms_filters',
            ],
        },
    },
]

WSGI_APPLICATION = 'ProjectInvoice.wsgi.application'

# --- Base de données ---
if os.environ.get('DATABASE_URL'):
    import dj_database_url
    DATABASES = {'default': dj_database_url.parse(os.environ['DATABASE_URL'], conn_max_age=600)}
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'invoicedb',
            'USER': 'guizo',
            'PASSWORD': '1234',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }

# --- Auth ---
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
     'OPTIONS': {'min_length': 6}},
]

# --- i18n ---
USE_I18N = True
USE_TZ = True
LANGUAGES = [('fr', 'Français'), ('en', 'English')]
LANGUAGE_CODE = 'fr'
TIME_ZONE = 'Africa/Douala'

LOCALE_PATHS = [Path(BASE_DIR.parent, "locale")]
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- Crispy ---
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# --- CORS ---
CORS_ALLOW_ALL_ORIGINS = DEBUG

# --- Email (dev) ---
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# --- Infos entreprise (utilisées dans le PDF) ---
COMPANY_NAME = os.environ.get('COMPANY_NAME', 'ABC BUSINESS')
COMPANY_ADDRESS = os.environ.get('COMPANY_ADDRESS', 'Yaoundé, Cameroun')
COMPANY_PHONE = os.environ.get('COMPANY_PHONE', '+237 6 XX XX XX XX')
COMPANY_EMAIL = os.environ.get('COMPANY_EMAIL', 'contact@abcbusiness.cm')
COMPANY_TAX_ID = os.environ.get('COMPANY_TAX_ID', 'M0123456789')
COMPANY_CURRENCY = 'FCFA'