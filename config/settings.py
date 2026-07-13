import os
from pathlib import Path
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load the environment variables from your .env file
load_dotenv(BASE_DIR / '.env')

# 1. SECURITY KEY: Use the .env value, but provide a safe development fallback
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-defense-donehub-change-this-before-production')

# 2. DEBUG MODE: Safely parse the string from .env to a Python Boolean
DEBUG = os.getenv('DEBUG', 'False') == 'True'

# 3. ALLOWED HOSTS: Allow your local machine and your Tailscale Funnel URL
# ALLOWED HOSTS
ALLOWED_HOSTS = os.getenv(
    "ALLOWED_HOSTS",
    "localhost,127.0.0.1,0.0.0.0", 
).split(",")

print("### ALLOWED HOSTS LOADED:", ALLOWED_HOSTS)

# Optional: If you want an absolute fallback for local rapid testing, 
# you can append '*' if DEBUG is True, but keep it strict for the funnel:
if DEBUG and not os.getenv('TAILSCALE_FUNNEL_URL'):
    ALLOWED_HOSTS.append('*')


# --- APPS CONFIGURATION ---
INSTALLED_APPS = [
    'daphne',  # Must be first!
    'channels',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Your custom apps
    'apps.dashboard',
    'apps.demo',
    'modules.occ',
]

# --- MIDDLEWARE ---
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# --- NETWORK ENGINE GATEWAYS ---
ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = 'config.asgi.application'

# --- TEMPLATE ENGINE (FIXED SYNTAX) ---
# --- TEMPLATE ENGINE (FIXED SYNTAX) ---
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # <-- Change this from [] to [BASE_DIR / "templates"]
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# --- DATABASE ---
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# --- GLOBALIZATION ---
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- STATIC FILES (THE JPG ROADMAP FIX) ---
STATIC_URL = "/static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = BASE_DIR / 'staticfiles'
CSRF_TRUSTED_ORIGINS = [
    "https://cyberbob-virtual-machine-1.tail79edaa.ts.net",
]
