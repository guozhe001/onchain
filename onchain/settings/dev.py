from .common import *  # noqa

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'crypto_hunter',
        'USER': 'root',
        'PASSWORD': '12345678',
        'HOST': '172.17.9.228',
        'PORT': '3306',
        'CHARSET': 'utf8mb4',
        'DEBUG': 'True',
    }
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "full": {"format": "%(asctime)s %(threadName)s [%(name)s] %(levelname)s: %(message)s"},
    },
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
    },
    "handlers": {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'full',
        },
        'file': {
            'level': 'INFO',
            'formatter': 'full',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': BASE_DIR.joinpath('logs/main.log'),
            'when': 'midnight',
            'interval': 1,
            'backupCount': 100,
        }
    },
    "loggers": {
        'hunter.*': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['console', 'file'],
            'propagate': True,
            'level': 'INFO',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
}
