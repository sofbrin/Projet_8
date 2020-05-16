from .development import *

SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = False
ALLOWED_HOSTS = ['51.210.4.42']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('db_name'),
        'USER': os.environ.get('db_user'),
        'PASSWORD': os.environ.get('db_password'),
        'HOST': '',
        'PORT': '5432',
    }
}
