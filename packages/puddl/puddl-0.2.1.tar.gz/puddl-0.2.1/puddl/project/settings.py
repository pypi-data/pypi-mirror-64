MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'puddl.project.urls'

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

WSGI_APPLICATION = 'puddl.project.wsgi.application'


def logging_config(log_level='INFO', log_sql=False):
    result = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            # https://docs.python.org/3/library/logging.html#logrecord-attributes
            'simple': {
                'format': '%(levelname)s %(message)s',
            },
            'standard': {
                'format': '[%(asctime)s] %(levelname)s %(name)s %(message)s',
                'datefmt': "%Y-%m-%d %H:%M:%S"
            },
        },
        'handlers': {
            'console': {
                'level': log_level,
                'class': 'logging.StreamHandler',
                'formatter': 'simple'
            },
        },
        'loggers': {
            # https://stackoverflow.com/a/31251707
            'puddl': {
                'handlers': ['console'],
                'level': log_level,
                'propagate': False,
            },
            'django': {
                'handlers': ['console'],
                'level': 'INFO',
                'propagate': True,
            },
        }
    }
    if log_sql:
        result['loggers']['django.db.backends'] = {
            'level': 'DEBUG',
        }
    return result


LOGGING = logging_config()


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
        'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
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

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'


# Queue Stuff
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': '_django_cache',
    }
}
# https://django-q.readthedocs.io/en/latest/configure.html
Q_CLUSTER = {
    'name': 'DjangORM',
    'orm': 'default',  # DB name
    'workers': 2,
    'timeout': 3600,  # scrapes take a while
    'retry': 3666,
}
