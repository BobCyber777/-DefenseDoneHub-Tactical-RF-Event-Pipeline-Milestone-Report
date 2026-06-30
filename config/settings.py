INSTALLED_APPS = [
    'daphne',  # Must be first!
    'channels',
    
    # Core Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Your custom modular app
    'apps.dashboard',
]

# Tell Django to use Channels/Daphne for processing network traffic
ASGI_APPLICATION = 'config.asgi.application'
